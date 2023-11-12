from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core import create_user, get_user_by_id, get_user_by_email, update_user, delete_user
from database import SessionLocal
from models import User as UserModel

user_router = APIRouter()

# Create a new user
@user_router.post("/users/", response_model=UserModel)
def create_new_user(user: UserModel):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    return create_user(db, user.name, user.email, user.password)

# Retrieve a user by ID
@user_router.get("/users/{user_id}", response_model=UserModel)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update user information
@user_router.put("/users/{user_id}", response_model=UserModel)
def update_existing_user(user_id: int, user: UserModel, db: Session = Depends(get_db)):
    db_user = get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return update_user(db, user_id, user.name, user.email, user.password)

# Delete a user
@user_router.delete("/users/{user_id}", response_model=UserModel)
def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    delete_user(db, user_id)
    return db_user
