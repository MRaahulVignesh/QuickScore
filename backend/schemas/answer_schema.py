from pydantic import BaseModel
from typing import Optional
from datetime import date

class CreateAnswer(BaseModel):
    student_id: int
    exam_id: int

    class Config:
        from_attributes = True 

class AnswerResponse(BaseModel):
    id: int
    student_name: str
    student_roll_no: str
    score: float
    confidence: float
    file_name: str 
        
class AnswerIndividualResponse(AnswerResponse):
    evaluation_details: str
    
    