from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from Database.db import Base





class ProductModel(Base):
    __tablename__ = "products"
    id:Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[float]
    count: Mapped[int]
    