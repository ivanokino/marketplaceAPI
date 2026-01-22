from typing import Annotated
from sqlalchemy.orm import DeclarativeBase  
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi import Depends


class Base(DeclarativeBase):
    pass

############     PRODUCTs    ##############################

product_engine = create_async_engine("sqlite+aiosqlite:///products.db")

product_session = async_sessionmaker(product_engine, expire_on_commit=False)

async def get_session_prod():
    async with product_session() as session:
        yield session

SessionDep_prod = Annotated[AsyncSession, Depends(get_session_prod)]

async def setup_prod_db():
    async with product_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


############     USERS    ##############################
    
users_engine = create_async_engine("sqlite+aiosqlite:///users.db")
user_session = async_sessionmaker(users_engine, expire_on_commit=False)
async def get_session_users():
    async with user_session() as session:
        yield session

SessionDep_users = Annotated[AsyncSession, Depends(get_session_users)]

async def setup_users_db():
     async with users_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


############     TESTS    ##############################

test_engine = create_async_engine("sqlite+aiosqlite:///prod_test.db")

test_session = async_sessionmaker(test_engine, expire_on_commit=False)
async def get_test_session():
    async with test_session() as session:
        yield session

async def init_test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



