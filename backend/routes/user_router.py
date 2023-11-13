
from fastapi import APIRouter, status, Query, Form
from fastapi.responses import JSONResponse, Response

from backend.schemas.user_schema import CreateUser, UpdateUser
from backend.core.user_core import UserCore
from backend.utils.errors import NotFoundError


user_router = APIRouter()

# Create a new user
@user_router.post("/")
def create_new_user(user: CreateUser):
    user_core = UserCore()
    try:
        user = user_core.create_user(name=user.name, email=user.email, password=user.password)
        response = JSONResponse(content=user, status_code=status.HTTP_201_CREATED)
    except NotFoundError as error:
        print(error)
        response = JSONResponse(content='{"message": "User"}', status_code=status.HTTP_404_NOT_FOUND_ERROR)   
    except Exception as error:
        print(error)
        response = JSONResponse(content='{"message": "Some Exception has occurred!!"}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response
    

# Retrieve a user by ID
@user_router.get("/{user_id}")
def get_user(user_id: int):
    user_core = UserCore()
    try:
        user = user_core.get_user_by_id(user_id)
        response = JSONResponse(content=user, status_code=status.HTTP_200_OK)
    except NotFoundError as error:
        print(error)
        response = JSONResponse(content='{"message": "User doesnot exist!!"}', status_code=status.HTTP_404_NOT_FOUND_ERROR) 
    except Exception as error:
        print(error)
        response = JSONResponse(content='{"message": "Some Exception has occurred!!"}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response

@user_router.get("/")
def get_user_by_email_endpoint(email: str = Query(..., description="User email")):
    user_core = UserCore()
    try:
        user = user_core.get_user_by_email(email)
        response = JSONResponse(content=user, status_code=status.HTTP_200_OK)
    except NotFoundError as error:
        print(error)
        response = JSONResponse(content='{"message": "User doesnot exist!!"}', status_code=status.HTTP_404_NOT_FOUND_ERROR) 
    except Exception as error:
        print(error)
        response = JSONResponse(content='{"message": "Some Exception has occurred!!"}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response

# Update user information
@user_router.put("/{user_id}")
def update_existing_user(user_id: int, user: UpdateUser):
    user_core = UserCore()
    try:
        user = user_core.update_user(user_id=user_id, name=user.name, email=user.email, password=user.password)
        if user is None:
            response = JSONResponse(content='{"message": "User not found"}', status_code=status.HTTP_404_NOT_FOUND)
        else:        
            response = JSONResponse(content=user, status_code=status.HTTP_200_OK)
    except Exception as error:
        print(error)
        response = JSONResponse(content='{"message": "Some Exception has occurred!!"}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response

# Delete a user
@user_router.delete("/{user_id}")
def delete_existing_user(user_id: int):
    user_core = UserCore()
    try:
        user_core.delete_user(user_id)
    except Exception as error:
        print(error)
        response = JSONResponse(content='{"message": "Some Exception has occurred!!"}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response

@user_router.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    user_core = UserCore()
    try:
        content = user_core.authenticate_user(email, password)
        response = JSONResponse(content=content, status_code=status.HTTP_200_OK)
    except Exception as error:
        print(error)
        response = JSONResponse(content='{"message": "Some Exception has occurred!!"}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response
