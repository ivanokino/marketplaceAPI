from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from Database.db import Base


class UserModel(Base):
    __tablename__="users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    password: Mapped[str]
    # owned_products: Mapped[List["ProductModel"]] = relationship(
    #     "ProductModel",
    #     back_populates="owner",
    #     cascade="all, delete-orphan"
    # )
    


class ProductModel(Base):
    __tablename__ = "products"
    id:Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[float]
    count: Mapped[int]
    owner_id: Mapped[int]
    # owner_id: Mapped[int] = mapped_column(
    #     ForeignKey("users.id"),  
    #     nullable=False
    # )
    
    # owner: Mapped["UserModel"] = relationship(
    #     "UserModel", 
    #     back_populates="owned_products"
    # )
    