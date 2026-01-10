from fastapi import FastAPI
import uvicorn
from Database.db import SessionDep_prod, setup_prod_db
from Schemas.ProductSchemes import ProductSchema
from sqlalchemy.future import select
from sqlalchemy import delete
from Models.ProductModels import ProductModel


app = FastAPI()

@app.post('/setup_prod')
async def setup_prod():
    await setup_prod_db()

@app.post("/post")
async def post_product(session:SessionDep_prod,product:ProductSchema):
    new_prod = ProductModel()
    new_prod.count = product.count
    new_prod.name = product.name
    new_prod.price = product.price
    session.add(new_prod)
    await session.commit()
    return {"product is posted": product}



@app.get("/")
async def main_page(session:SessionDep_prod):
    result = await session.execute(select(ProductModel))
    products = result.scalars().all()
    return {"products": products}


@app.post("/del")
async def post_product(session:SessionDep_prod,id:int):
    product = await session.execute(select(ProductModel).where(ProductModel.id==id))
    query= delete(ProductModel).where(ProductModel.id==id)
    await session.execute(query)
    await session.commit()
    product = product.scalar_one_or_none()
    return {"product is deleted": product}

if __name__ == "__main__":
    uvicorn.run(app=app)