from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    username: str = Field(max_length=15, min_length=1) 
    password: str = Field(min_length=2, max_length=15)
    