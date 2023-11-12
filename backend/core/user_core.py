from sqlalchemy.orm import Session
from models import User

class UserCore:

    def __init__(self):
        self.user_dao = UserDao()

    # Create a new user
    def create_user(self, name: str, email: str, password: str):
        user = self.user_dao.create_user(name, email, password)
        return user

    # Retrieve a user by ID
    def get_user_by_id(self, user_id: int):
        user = self.user_dao.get_user_by_id(user_id)
        return user

    # Retrieve a user by email
    def get_user_by_email(self, email: str):
        user = self.user_dao.get_user_by_email(email)
        return user

    # Update user information
    def update_user(self, user_id: int, name: str, email: str, password: str):
        user = self.user_dao.update_user(user_id, name, email, password)
        return user

    # Delete a user
    def delete_user(self, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
        return True
