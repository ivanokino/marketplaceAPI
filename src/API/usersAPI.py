from authx import AuthX, AuthXConfig
from fastapi import APIRouter, HTTPException, Response
from Schemas.UserSchemas import UserSchema
from Database.db import SessionDep_users, setup_users_db
from Models.APImodels import UserModel
from sqlalchemy.future import select


router = APIRouter()


config = AuthXConfig()
config.JWT_SECRET_KEY = "secretkey"
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_ACCESS_COOKIE_NAME = "JWT_TOKEN"
config.JWT_COOKIE_CSRF_PROTECT = False


security = AuthX(config=config)


@router.post("/setup_users")
async def setup_users():
    await setup_users_db()


@router.post("/register")
async def register(user:UserSchema, session:SessionDep_users):
    result = await session.execute(select(UserModel).where(UserModel.username == user.username))
    existing_user = result.scalar_one_or_none() 

    if existing_user:
        raise HTTPException(status_code=400, detail="User is already exist")
    new_user = new_user = UserModel(
        username=user.username,
        password=user.password
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return {"name": new_user.username, "id": new_user.id}


@router.post("/login")
async def register(user:UserSchema, session:SessionDep_users,  respone: Response):
    result = await session.execute(select(UserModel).where(UserModel.username == user.username))
    existing_user = result.scalar_one_or_none() 
    
    if existing_user and existing_user.password == user.password:
        token = security.create_access_token(uid=str(existing_user.id))
        respone.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
    
    
        return {"response": "login succesful"}
    raise HTTPException(status_code=401, detail="incorrect username or password")