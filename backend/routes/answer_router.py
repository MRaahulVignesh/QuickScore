from fastapi import APIRouter, status, Query, Form, File, UploadFile
from fastapi.responses import JSONResponse, Response

from backend.schemas.answer_schema import CreateAnswer
from backend.core.answer_core import AnswerCore
from backend.utils.errors import NotFoundError
from pydantic import ValidationError

import pdfplumber
import tempfile
import io
import json

answer_router = APIRouter()

@answer_router.post("/")
async def create_answer(file: UploadFile = File(...), answer_data: str = Form(...)):
    try:
        if not file.filename.endswith(".pdf"):
            return JSONResponse(content='{"message": "Only PDF files are allowed."}', status_code=status.HTTP_400_BAD_REQUEST)
    
        # Read the uploaded PDF file as bytes
        pdf_data = await file.read()

        # Process the PDF data in memory
        # For example, you can use a library like pdfplumber to extract text
        # Here's a simple example using pdfplumber:

        with pdfplumber.open(io.BytesIO(pdf_data)) as pdf:
            answer_pdf = ""
            for page in pdf.pages:
                answer_pdf += page.extract_text()
    
    except Exception as error:
        print(error)
        return JSONResponse(content='{"message": "Some Exception has occurred!!"}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Parse the JSON data
    try:
        parsed_answer_data = json.loads(answer_data)
    except json.JSONDecodeError as e:
        print(e)
        return JSONResponse(content='{"message": "Invalid JSON data!!"}', status_code=status.HTTP_400_BAD_REQUEST)

    # Validate the parsed JSON data using Pydantic
    try:
        validated_answer_data = CreateAnswer(**parsed_answer_data)
    except ValidationError as e:
        print(e)
        return JSONResponse(content='{"message": "Invalid JSON data!!"}', status_code=status.HTTP_400_BAD_REQUEST)
                
    answer_core = AnswerCore()
    try:
        answer = answer_core.create_answer(validated_answer_data, answer_pdf)
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
        response = JSONResponse(content='{"message": "Answer doesnot exist!!"}', status_code=status.HTTP_404_NOT_FOUND) 
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