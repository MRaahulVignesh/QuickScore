from pydantic import BaseModel
from typing import Optional

class CreateContext(BaseModel):
    name: str
    comments: str
    user_id: int

    class Config:
        from_attributes = True

class ContextResponse(CreateContext):
    id: int

