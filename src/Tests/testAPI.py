import time
from httpx import ASGITransport, AsyncClient
import jwt
import pytest
from Database.db import setup_prod_db
from main import app


def get_JWT():
    payload = {
        "sub": '1',  
        "exp": int(time.time()) + 3600,  
        "iat": int(time.time()), 
        "type": "access",
        "fresh": False,
        "jti": "test-jti"
    }    
    secret_key = "secretkey"
    fake_token = jwt.encode(payload, secret_key, algorithm="HS256")
    return fake_token

item_test = {
    "id":1,
    'name':"test prod", 
    'price':1000,
    'count':10,
    'owner_id':1,
}

    


@pytest.mark.asyncio()
async def test_main_page():
    await setup_prod_db()
    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test",
                           ) as ac:   
        
        response = await ac.get("/")
        assert response.status_code == 200   


@pytest.mark.asyncio()
async def test_post_product():

    await setup_prod_db()

    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test", 
                           ) as ac:   
        ac.cookies.set("JWT_TOKEN", get_JWT())
        response = await ac.post(url="/post"
                                 , json=item_test)
        assert response.status_code == 200  

@pytest.mark.asyncio()
async def test_delete_product():
    await setup_prod_db()
    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test", 
                           ) as ac:   
        ac.cookies.set("JWT_TOKEN", get_JWT())
        response = await ac.post(url="/del?id=2"
                                 )
        assert response.status_code in [200,404]  