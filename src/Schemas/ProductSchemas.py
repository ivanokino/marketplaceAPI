from pydantic import BaseModel, Field

class ProductSchema(BaseModel):
    name: str = Field(max_length=15, min_length=2) 
    price: float = Field(ge=0)
    count: int = Field(ge=1)
