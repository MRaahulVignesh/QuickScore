from fastapi import APIRouter, status, Query, Form, File, UploadFile
from fastapi.responses import JSONResponse, Response

from backend.schemas.exam_schema import CreateExam
from backend.core.exam_core import ExamCore
from backend.utils.errors import NotFoundError

from pydantic import ValidationError

import pdfplumber
import tempfile
import io
import json

exam_router = APIRouter()

@exam_router.post("/")
async def create_new_exam(file: UploadFile = File(...), exam: str = Form(...)):

    try:
        if not file.filename.endswith(".pdf"):
            return JSONResponse(content='{"message": "Only PDF files are allowed."}', status_code=status.HTTP_400_BAD_REQUEST)
    
        # Read the uploaded PDF file as bytes
        pdf_data = await file.read()

        # Process the PDF data in memory
        # For example, you can use a library like pdfplumber to extract text
        # Here's a simple example using pdfplumber:

        with pdfplumber.open(io.BytesIO(pdf_data)) as pdf:
            pdf_text = ""
            for page in pdf.pages:
                pdf_text += page.extract_text()

    except Exception as error:
        print(error)
        return JSONResponse(content='{"message": "Some Exception has occurred!!"}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Parse the JSON data
    try:
        parsed_exam = json.loads(exam)
    except json.JSONDecodeError as e:
        print(e)
        return JSONResponse(content='{"message": "Invalid JSON data!!"}', status_code=status.HTTP_400_BAD_REQUEST)

    # Validate the parsed JSON data using Pydantic
    try:
        validated_exam = CreateExam(**parsed_exam)
    except ValidationError as e:
        print(e)
        return JSONResponse(content='{"message": "Invalid JSON data!!"}', status_code=status.HTTP_400_BAD_REQUEST)


    exam_core = ExamCore()
    try:
        exam_res = exam_core.create_exam(validated_exam, pdf_text)
        response = JSONResponse(content=exam_res, status_code=status.HTTP_200_OK)
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
        response = JSONResponse(content='{"message": "Exam doesnot exist!!"}', status_code=status.HTTP_404_NOT_FOUND_ERROR) 
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
    except Exception as error:
        response = JSONResponse(content='{"message": "Some Exception has occurred!!"}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response