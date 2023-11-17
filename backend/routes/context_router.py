from fastapi import APIRouter, status, Query, Form, File, UploadFile
from fastapi.responses import JSONResponse, Response

from backend.schemas.context_schema import CreateContext
from backend.core.context_core import ContextCore
from backend.utils.errors import NotFoundError
from pydantic import ValidationError
from langchain.document_loaders import PyPDFLoader

import io
import json
import tempfile

context_router = APIRouter()

@context_router.post("/")
async def create_context(file: UploadFile = File(...), context: str = Form(...)):
    try:
        if not file.filename.endswith(".pdf"):
            return JSONResponse(content='{"message": "Only PDF files are allowed."}', status_code=status.HTTP_400_BAD_REQUEST)
        filename = str(file.filename)
        context_pdf = None
        with tempfile.NamedTemporaryFile(delete=True) as temp_file:
            # Read the content from the uploaded file
            contents = await file.read()

            # Write the content to the temporary file
            temp_file.write(contents)
            temp_file.flush()

            # Get the path of the temporary file
            temp_file_path = temp_file.name
            
            loader = PyPDFLoader(temp_file_path)
            context_pdf = loader.load()
        
    except Exception as error:
        print(error)
        return JSONResponse(content='{"message": "Some Exception has occurred!!"}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Parse the JSON data
    try:
        parsed_context_data = json.loads(context)
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
        context = context_core.create_context(input=validated_context_data, context_pdf=context_pdf, filename=filename)
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
def get_contexts_by_exam_id(user_id: str = Query(..., description="Exam Id")):
    context_core = ContextCore()
    try:
        contexts = context_core.get_contexts_by_user_id(user_id)
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