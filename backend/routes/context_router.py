from fastapi import APIRouter, status, Query, Form, File, UploadFile
from fastapi.responses import JSONResponse, Response

from backend.schemas.context_schema import CreateContext
from backend.core.context_core import ContextCore
from backend.utils.errors import NotFoundError
from pydantic import ValidationError

import pdfplumber
import tempfile
import io
import json

context_router = APIRouter()

@context_router.post("/")
async def create_context(file: UploadFile = File(...), context_data: str = Form(...)):
    print(file, type(file))
    try:
        if not file.filename.endswith(".pdf"):
            return JSONResponse(content='{"message": "Only PDF files are allowed."}', status_code=status.HTTP_400_BAD_REQUEST)
    
        # Read the uploaded PDF file as bytes
        pdf_data = await file.read()

        # Process the PDF data in memory
        # For example, you can use a library like pdfplumber to extract text
        # Here's a simple example using pdfplumber:

        with pdfplumber.open(io.BytesIO(pdf_data)) as pdf:
            context_pdf = ""
            for page in pdf.pages:
                context_pdf += page.extract_text()
    
    except Exception as error:
        print(error)
        return JSONResponse(content='{"message": "Some Exception has occurred!!"}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Parse the JSON data
    try:
        parsed_context_data = json.loads(context_data)
    except json.JSONDecodeError as e:
        print(e)
        return JSONResponse(content='{"message": "Invalid JSON data!!"}', status_code=status.HTTP_400_BAD_REQUEST)

    # Validate the parsed JSON data using Pydantic
    try:
        validated_context_data = CreateContext(**parsed_context_data)
    except ValidationError as e:
        print(e)
        return JSONResponse(content='{"message": "Invalid JSON data!!"}', status_code=status.HTTP_400_BAD_REQUEST)
                
    context_core = ContextCore()
    try:
        context = context_core.create_context(validated_context_data, context_pdf)
        return JSONResponse(content=context, status_code=status.HTTP_200_OK)
    except Exception as error:
        print(error)
        return JSONResponse(content='{"message": "Some Exception has occurred!!"}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# Retrieve a user by ID
@context_router.get("/{context_id}")
def get_context(context_id: int):
                
    context_core = ContextCore()
    try:
        context = context_core.get_context_by_id(context_id)
        response = JSONResponse(content=context, status_code=status.HTTP_200_OK)
    except NotFoundError as error:
        print(error)
        response = JSONResponse(content='{"message": "Context doesnot exist!!"}', status_code=status.HTTP_404_NOT_FOUND) 
    except Exception as error:
        print(error)
        response = JSONResponse(content='{"message": "Some Exception has occurred!!"}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response

@context_router.get("/")
def get_contexts_by_exam_id(exam_id: str = Query(..., description="Exam Id")):
    context_core = ContextCore()
    try:
        contexts = context_core.get_contexts_by_exam_id(exam_id)
        response = JSONResponse(content=contexts, status_code=status.HTTP_200_OK)
    except Exception as error:
        print(error)
        response = JSONResponse(content='{"message": "Some Exception has occurred!!"}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response

# Delete a user
@context_router.delete("/{id}")
def delete_context(id: int):
    context_core = ContextCore()
    try:
        context_core.delete_context(id)
        response = Response(status_code=status.HTTP_200_OK)       
    except Exception as error:
        response = JSONResponse(content='{"message": "Some Exception has occurred!!"}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response