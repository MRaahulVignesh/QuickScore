from pydantic import BaseModel
from typing import Optional

class CreateStudent(BaseModel):
    name: str
    email: str
    roll_no: str
    user_id: int

    class Config:
        from_attributes = True

class StudentResponse(CreateStudent):
    id: int

