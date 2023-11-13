from sqlalchemy.orm import Session
from sqlalchemy import exc

from backend.utils.db_conn import postgres_conn  
from backend.utils.errors import DatabaseError, DuplicateError, NotFoundError
from backend.models.models import UserModel

class UserDao:
    def __init__(self):
        self.db = postgres_conn.get_db()

    # Create a new user
    def create_user(self, name: str, email: str, password: str):
        try:
            user = UserModel(name=name, email=email, password=password)
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        except exc.IntegrityError as error:
            print(error)
            raise DuplicateError("Similar Record already exists!")
        except Exception as error:
            print(error)
            raise DatabaseError("DB operation Failed: Create_User")
        finally:
            self.db.close()
        print(user)
        return user

    # Retrieve a user by ID
    def get_user_by_id(self, user_id: int):
        try:
            user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
            if user is None:
                raise NotFoundError("User doesnot exist!")
        except Exception as error:
            print(error)
            raise DatabaseError("DB operation Failed: Get_User_By_Id")
        return user

    # Retrieve a user by email
    def get_user_by_email(self, email: str):
        try:
            user = self.db.query(UserModel).filter(UserModel.email == email).first()
            if user is None:
                raise NotFoundError("User doesnot exist!")
        except Exception as error:
            print(error)
            raise DatabaseError("DB operation Failed: Get_User_By_Email")
        return user

    # Update user information
    def update_user(self, user_id: int, name: str, email: str, password: str):
        try:
            user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
            if user:
                user.name = name
                user.email = email
                user.password = password
                self.db.commit()
                self.db.refresh(user)
        except Exception as error:
            print(error)
            raise DatabaseError("DB operation Failed: Update_User")
        return user

    # Delete a user
    def delete_user(self, user_id: int):
        try:
            user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
            if user is None:
                raise NotFoundError("User doesnot exist!")
            self.db.delete(user)
            self.db.commit()
        except Exception as error:
            print(error)
            raise DatabaseError("DB operation Failed: Delete_User")
        return True
