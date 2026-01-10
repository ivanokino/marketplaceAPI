from typing import Annotated
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi import Depends

class Base(DeclarativeBase):
    pass

users_engine = create_async_engine("sqlite+aiosqlite:///users.db")

product_engine = create_async_engine("sqlite+aiosqlite:///products.db")

product_session = async_sessionmaker(product_engine, expire_on_commit=False)

async def get_session():
    async with product_session() as session:
        yield session

SessionDep_prod = Annotated[AsyncSession, Depends(get_session)]

async def setup_prod_db():
    async with product_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)





