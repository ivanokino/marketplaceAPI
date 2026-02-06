from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select

from Schemas.ProductSchemas import ProductSchema
from Database.db import SessionDep_prod, setup_prod_db, SessionDep_users
from API.usersAPI import security, get_current_user_id
from Models.APImodels import ProductModel, UserModel

router = APIRouter()

@router.post('/setup_prod')
async def setup_prod():
    await setup_prod_db()

@router.post("/post", dependencies=[Depends(security.access_token_required)])
async def post_product(session:SessionDep_prod,product:ProductSchema,
                       user_id = Depends(get_current_user_id)):
    new_prod = ProductModel(
        count=product.count,
        name = product.name,
        price = product.price,
        owner_id = int(user_id)
    )

    session.add(new_prod)
    await session.commit()
    return {"product is posted": new_prod}


@router.post("/del", dependencies=[Depends(security.access_token_required)])
async def delete_product(session:SessionDep_prod,id:int,
                         user_id = Depends(get_current_user_id)):
    product = await session.execute(select(ProductModel).where(ProductModel.id==id))
    
    product= product.scalar_one_or_none()
    if not product: 
        raise HTTPException(status_code=404, detail="Item isnt found")
    
    if product.owner_id == int(user_id):
        query= delete(ProductModel).where(ProductModel.id==id)
        await session.execute(query)
        await session.commit()
        return {"product is deleted": product}
    
    raise HTTPException(status_code=403, detail="Its not your item")

@router.post("/track", dependencies=[Depends(security.access_token_required)])
async def track(session_prod: SessionDep_prod,
                id:int,
                session_user: SessionDep_users,
                user_id = Depends(get_current_user_id)):
    
    product = await session_prod.execute(select(ProductModel).where(ProductModel.id == id))
    product = product.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=403, detail="Product not found")
    user = await session_user.execute(select(UserModel).where(UserModel.id == user_id))
    user = user.scalar_one_or_none()
    user.tracked.append(product.id)

    await session_user.commit()
    await session_user.refresh(user)
    return {"message": "Product added to tracked", "tracked_count": len(user.tracked)}



    
    
    