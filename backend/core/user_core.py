import jwt
import datetime

from backend.utils.errors import NotFoundError, AuthenticationError
from backend.dao.user_dao import UserDao
from backend.schemas.user_schema import UserResponse
from backend.config.config import config

class UserCore:

    def __init__(self):
        self.user_dao = UserDao()

    # Create a new user
    def create_user(self, name: str, email: str, password: str):
        user = self.user_dao.create_user(name, email, password)
        user = UserResponse.model_validate(user).model_dump(mode="json")
        return user

    # Retrieve a user by ID
    def get_user_by_id(self, user_id: int):
        user = self.user_dao.get_user_by_id(user_id)
        if user is None:
            raise NotFoundError("User doesnot exist!")
        user = UserResponse.model_validate(user).model_dump(mode="json")
        return user

    # Retrieve a user by email
    def get_user_by_email(self, email: str):
        user = self.user_dao.get_user_by_email(email)
        if user is None:
            raise NotFoundError("User doesnot exist!")
        user = UserResponse.model_validate(user).model_dump(mode="json")
        return user

    # Update user information
    def update_user(self, user_id: int, name: str, email: str, password: str):
        user = self.user_dao.update_user(user_id, name, email, password)
        user = UserResponse.model_validate(user).model_dump(mode="json")
        return user

    # Delete a user
    def delete_user(self, user_id: int):
        user = self.user_dao.delete_user(user_id)
        user = UserResponse.model_validate(user).model_dump(mode="json")
        return True
    
    def authenticate_user(self, email, password):
        user = self.user_dao.get_user_by_email(email)
        if user is None:
            raise AuthenticationError("Error in email or password!")
        actual_password = str(user.__dict__["password"])
        if actual_password != password:
            raise AuthenticationError("Error in email or password!")
        secret_key = config.SECRET_KEY
        user = user.__dict__
        payload = {
            "user_id": user["id"],
            "email": user["email"],
            "name": user["name"]
        }
        return payload
