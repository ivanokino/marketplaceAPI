from unittest.mock import AsyncMock, patch
from authx import AuthX
from httpx import ASGITransport, AsyncClient
import pytest
from Database.db import setup_prod_db
from main import app
from API.usersAPI import get_current_user_id, security


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


# @pytest.mark.asyncio()
# async def test_post_product():
#     await setup_prod_db()
#     async with AsyncClient(transport=ASGITransport(app=app),
#                            base_url="http://test", 
#                            ) as ac:   
        
#         response = await ac.post(url="/post"
#                                  , json=item_test)
#         assert response.status_code == 200  