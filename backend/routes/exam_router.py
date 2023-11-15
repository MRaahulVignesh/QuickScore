from fastapi import APIRouter, status, Query, Form
from fastapi.responses import JSONResponse, Response

from backend.schemas.exam_schema import CreateExam
from backend.core.exam_core import ExamCore
from backend.utils.errors import NotFoundError

exam_router = APIRouter()

@exam_router.post("/")
def create_new_exam(exam: CreateExam):
    exam_core = ExamCore()
    try:
        exam = exam_core.create_exam(exam)
        response = JSONResponse(content=exam, status_code=status.HTTP_200_OK)
    except Exception as error:
        print(error)
        response = JSONResponse(content='{"message": "Some Exception has occurred!!"}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response
    

# Retrieve a user by ID
@exam_router.get("/{exam_id}")
def get_exam(exam_id: int):
    exam_core = ExamCore()
    try:
        exam = exam_core.get_exam_by_id(exam_id)
        response = JSONResponse(content=exam, status_code=status.HTTP_200_OK)
    except NotFoundError as error:
        print(error)
        response = JSONResponse(content='{"message": "Exam doesnot exist!!"}', status_code=status.HTTP_404_NOT_FOUND) 
    except Exception as error:
        print(error)
        response = JSONResponse(content='{"message": "Some Exception has occurred!!"}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response

@exam_router.get("/")
def get_exams_by_user_id(user_id: str = Query(..., description="User Id")):
    exam_core = ExamCore()
    try:
        exams = exam_core.get_exams_by_user_id(user_id)
        response = JSONResponse(content=exams, status_code=status.HTTP_200_OK)
    except Exception as error:
        print(error)
        response = JSONResponse(content='{"message": "Some Exception has occurred!!"}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response

# Delete a user
@exam_router.delete("/{id}")
def delete_exam(id: int):
    exam_core = ExamCore()
    try:
        exam_core.delete_exam(id)
        response = Response(status_code=status.HTTP_200_OK)
    except NotFoundError as error:
        print(error)
        response = JSONResponse(content='{"message": "Exam doesnot exist!!"}', status_code=status.HTTP_404_NOT_FOUND)           
    except Exception as error:
        response = JSONResponse(content='{"message": "Some Exception has occurred!!"}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response