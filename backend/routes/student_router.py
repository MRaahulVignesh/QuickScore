from fastapi import APIRouter, status, Query, Form
from fastapi.responses import JSONResponse, Response

from backend.schemas.student_schema import CreateStudent
from backend.core.student_core import StudentCore
from backend.utils.errors import NotFoundError

student_router = APIRouter()

@student_router.post("/")
def create_student(input: CreateStudent):
    student_core = StudentCore()
    try:
        student = student_core.create_student(input)
        response = JSONResponse(content=student, status_code=status.HTTP_200_OK)
    except Exception as error:
        print(error)
        response = JSONResponse(content='{"message": "Some Exception has occurred!!"}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response
    

@student_router.get("/{student_id}")
def get_student(student_id: int):
    student_core = StudentCore()
    try:
        student = student_core.get_student_by_id(student_id)
        response = JSONResponse(content=student, status_code=status.HTTP_200_OK)
    except NotFoundError as error:
        print(error)
        response = JSONResponse(content='{"message": "Student doesnot exist!!"}', status_code=status.HTTP_404_NOT_FOUND) 
    except Exception as error:
        print(error)
        response = JSONResponse(content='{"message": "Some Exception has occurred!!"}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response

@student_router.get("/")
def get_students_by_user_id(user_id: str = Query(..., description="User Id")):
    student_core = StudentCore()
    try:
        students = student_core.get_students_by_user_id(user_id)
        response = JSONResponse(content=students, status_code=status.HTTP_200_OK)
    except NotFoundError as error:
        print(error)
        response = JSONResponse(content='{"message": "Student doesnot exist!!"}', status_code=status.HTTP_404_NOT_FOUND) 
    except Exception as error:
        print(error)
        response = JSONResponse(content='{"message": "Some Exception has occurred!!"}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response

# Delete a user
@student_router.delete("/{id}")
def delete_student(id: int):
    student_core = StudentCore()
    try:
        student_core.delete_student(id)
        response = Response(status_code=status.HTTP_200_OK)  
    except NotFoundError as error:
        print(error)
        response = JSONResponse(content='{"message": "Student doesnot exist!!"}', status_code=status.HTTP_404_NOT_FOUND)      
    except Exception as error:
        print(error)
        response = JSONResponse(content='{"message": "Some Exception has occurred!!"}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response