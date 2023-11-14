from fastapi import APIRouter, status, Query, Form
from fastapi.responses import JSONResponse, Response

from backend.schemas.answer_schema import CreateAnswer
from backend.core.answer_core import AnswerCore
from backend.utils.errors import NotFoundError

answer_router = APIRouter()

@answer_router.post("/")
def create_answer(answer: CreateAnswer):
    answer_core = AnswerCore()
    try:
        answer = answer_core.create_answer(answer)
        return JSONResponse(content=answer, status_code=status.HTTP_200_OK)
    except Exception as error:
        print(error)
        return JSONResponse(content='{"message": "Some Exception has occurred!!"}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# Retrieve a user by ID
@answer_router.get("/{answer_id}")
def get_answer(answer_id: int):
    answer_core = AnswerCore()
    try:
        answer = answer_core.get_answer_by_id(answer_id)
        response = JSONResponse(content=answer, status_code=status.HTTP_200_OK)
    except NotFoundError as error:
        print(error)
        response = JSONResponse(content='{"message": "Answer doesnot exist!!"}', status_code=status.HTTP_404_NOT_FOUND_ERROR) 
    except Exception as error:
        print(error)
        response = JSONResponse(content='{"message": "Some Exception has occurred!!"}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response

@answer_router.get("/")
def get_answers_by_exam_id(exam_id: str = Query(..., description="Exam Id")):
    answer_core = AnswerCore()
    try:
        answers = answer_core.get_answers_by_exam_id(exam_id)
        response = JSONResponse(content=answers, status_code=status.HTTP_200_OK)
    except Exception as error:
        print(error)
        response = JSONResponse(content='{"message": "Some Exception has occurred!!"}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response

# Delete a user
@answer_router.delete("/{id}")
def delete_answer(id: int):
    answer_core = AnswerCore()
    try:
        answer_core.delete_answer(id)
        response = Response(status_code=status.HTTP_200_OK)       
    except Exception as error:
        response = JSONResponse(content='{"message": "Some Exception has occurred!!"}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response