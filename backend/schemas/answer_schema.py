from pydantic import BaseModel
from typing import Optional
from datetime import date

class CreateAnswer(BaseModel):
    student_id: int
    exam_id: int
    score: Optional[float] = None

    class Config:
        from_attributes = True 

class AnswerResponse(CreateAnswer):
    id: int