from pydantic import BaseModel
from typing import Optional
from datetime import date

class CreateAnswer(BaseModel):
    student_id: int
    exam_id: int
    score: Optional[float] = None

    class Config:
        from_attributes = True 

class AnswerResponse(BaseModel):
    id: int
    student_name: str
    student_roll_no: str
    score: float
    confidence: float

    class Config:
        from_attributes = True     
    
    