from typing import List
# from sqlalchemy import ForeignKey
from sqlalchemy import JSON, Integer
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from Database.db import Base
from werkzeug.security import generate_password_hash, check_password_hash

class UserModel(Base):
    __tablename__="users"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    hash_password: Mapped[str] = mapped_column(nullable=False)
    contacts: Mapped[str] = mapped_column(nullable=False)
    tracked: Mapped[List[int]] = mapped_column(MutableList.as_mutable(JSON), default=list)

    def set_hashed_password(self, password):
        self.hash_password =  generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hash_password, password)



class ProductModel(Base):
    __tablename__ = "products"
    id:Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    count: Mapped[int] = mapped_column(nullable=False)
    owner_id: Mapped[int] = mapped_column(nullable=False)
  