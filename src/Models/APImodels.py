# from typing import List
# from sqlalchemy import ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from Database.db import Base
from werkzeug.security import generate_password_hash, check_password_hash

class UserModel(Base):
    __tablename__="users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    hash_password: Mapped[str]

    def set_hashed_password(self, password):
        self.hash_password =  generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hash_password, password)
    
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
    