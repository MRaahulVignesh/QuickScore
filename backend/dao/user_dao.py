from sqlalchemy.orm import Session
from models import User

class UserDao:
    def __init__(self, db):
        self.db = db

    # Create a new user
    def create_user(self, name: str, email: str, password: str):
        user = User(name=name, email=email, password=password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    # Retrieve a user by ID
    def get_user_by_id(self, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    # Retrieve a user by email
    def get_user_by_email(self, email: str):
        return db.query(User).filter(User.email == email).first()

    # Update user information
    def update_user(self, user_id: int, name: str, email: str, password: str):
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.name = name
            user.email = email
            user.password = password
            db.commit()
            db.refresh(user)
        return user

    # Delete a user
    def delete_user(self, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
        return True
