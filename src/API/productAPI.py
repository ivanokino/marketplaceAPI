from fastapi import APIRouter, Depends
from sqlalchemy import delete, select

from Schemas.ProductSchemas import ProductSchema
from Database.db import SessionDep_prod, setup_prod_db, SessionDep_prod
from API.usersAPI import security, get_current_user_id
from Models.APImodels import ProductModel

router = APIRouter()

@router.post('/setup_prod')
async def setup_prod():
    await setup_prod_db()

@router.post("/post", dependencies=[Depends(security.access_token_required)])
async def post_product(session:SessionDep_prod,product:ProductSchema,
                       user_id: int = Depends(get_current_user_id)):
    new_prod = ProductModel(
        count=product.count,
        name = product.name,
        price = product.price,
        owner_id = user_id
    )

    session.add(new_prod)
    await session.commit()
    return {"product is posted": new_prod}


@router.post("/del", dependencies=[Depends(security.access_token_required)])
async def post_product(session:SessionDep_prod,id:int):
    product = await session.execute(select(ProductModel).where(ProductModel.id==id))
    query= delete(ProductModel).where(ProductModel.id==id)
    await session.execute(query)
    await session.commit()
    product = product.scalar_one_or_none()
    return {"product is deleted": product}