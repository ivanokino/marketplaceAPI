from fastapi import Depends, FastAPI
import uvicorn
from Database.db import SessionDep_prod, setup_prod_db
from Schemas.ProductSchemas import ProductSchema
from sqlalchemy.future import select
from sqlalchemy import delete
from Models.APImodels import ProductModel
from API.usersAPI import router as users_router, security

app = FastAPI()
app.include_router(users_router)

@app.post('/setup_prod')
async def setup_prod():
    await setup_prod_db()

@app.post("/post", dependencies=[Depends(security.access_token_required)])
async def post_product(session:SessionDep_prod,product:ProductSchema):
    new_prod = ProductModel(
        count=product.count,
        name = product.name,
        price = product.price
    )

    session.add(new_prod)
    await session.commit()
    return {"product is posted": product}



@app.get("/")
async def main_page(session:SessionDep_prod):
    result = await session.execute(select(ProductModel))
    products = result.scalars().all()
    return {"products": products}


@app.post("/del", dependencies=[Depends(security.access_token_required)])
async def post_product(session:SessionDep_prod,id:int):
    product = await session.execute(select(ProductModel).where(ProductModel.id==id))
    query= delete(ProductModel).where(ProductModel.id==id)
    await session.execute(query)
    await session.commit()
    product = product.scalar_one_or_none()
    return {"product is deleted": product}

if __name__ == "__main__":
    uvicorn.run(app=app)