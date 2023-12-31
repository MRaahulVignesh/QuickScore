from pydantic import BaseModel
from typing import Optional
from datetime import date

class CreateExam(BaseModel):
    name: str
    description: str
    total_marks: float
    conducted_date: date
    user_id: int
    context_id: Optional[int]
    
    class Config:
        from_attributes = True 

class ExamResponse(CreateExam):
    id: int
    file_name: str