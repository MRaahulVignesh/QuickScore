from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Boolean, Table, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

from backend.utils.db_conn import Base

# Define the User model
class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

# Define the Exam model
class ExamModel(Base):
    __tablename__ = 'exams'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    conducted_date = Column(Date)
    description = Column(String(255))
    total_marks = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    answer_key = Column(JSON, default={})
    # context_id = Column(Integer, ForeignKey('contexts.id'), nullable=True)

# Define the Student model
class StudentModel(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    roll_no = Column(String(50), unique=True)
    email = Column(String(255), nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))

# Define the Answer model
class AnswerModel(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    exam_id = Column(Integer, ForeignKey('exams.id'))
    score = Column(Float, default=0.0)
    
# Define the Answer model
class ContextModel(Base):
    __tablename__ = 'contexts'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    comments = Column(String(255), nullable=True)
    context_key = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))    