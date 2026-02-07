from pydantic import BaseModel, Field




class UserSchema(BaseModel):
    password: str = Field(min_length=2, max_length=15)    

class UserResponse(BaseModel):
    id: int
    username: str
    contacts: str