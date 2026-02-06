from fastapi import FastAPI
import uvicorn

from sqlalchemy.future import select
from Models.APImodels import ProductModel
from Database.db import SessionDep_prod
from API.usersAPI import router as users_router
from API.productAPI import router as product_router

app = FastAPI()
app.include_router(users_router)
app.include_router(product_router)

@app.get("/")
async def main_page(session:SessionDep_prod):
    result = await session.execute(select(ProductModel))
    products = result.scalars().all()
    return {"products": products}



if __name__ == "__main__":
    uvicorn.run(app=app)    