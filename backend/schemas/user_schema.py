from pydantic import BaseModel
from typing import Optional

class CreateUser(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        from_attributes = True

class UserResponse(CreateUser):
    id: int

class UpdateUser(BaseModel):
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]

    class Config:
        from_attributes = True    