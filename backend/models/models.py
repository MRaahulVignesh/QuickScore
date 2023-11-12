from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Modify the User class to use the association tables
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

    # Establish a many-to-many relationship between User and Exam
    exams = relationship("Exam", secondary=user_exam_association, back_populates="users")

    # Establish a one-to-many relationship between User and Student
    students = relationship("Student", secondary=user_student_association, back_populates="user")

# Modify the Exam class to include a many-to-many relationship with User
class Exam(Base):
    __tablename__ = 'exams'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    conducted_date = Column(DateTime, default=func.now())
    total_marks = Column(Float, nullable=False)
    description = Column(String(255))

    # Establish a many-to-one relationship between Exam and Answer
    answers = relationship("Answer", back_populates="exam")

    # Establish a many-to-many relationship between User and Exam
    users = relationship("User", secondary=user_exam_association, back_populates="exams")

# Modify the Student class to include a many-to-one relationship with User
class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    roll_no = Column(String(50), unique=True)
    email = Column(String(255), nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    # Establish a many-to-one relationship between User and Student
    user = relationship("User", back_populates="students")

# Define the Answer model
class Answer(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    exam_id = Column(Integer, ForeignKey('exams.id'))
    evaluation_status = Column(Boolean, default=False)
    score = Column(Float)

    # Establish a many-to-one relationship between Student and Answer
    student = relationship("Student", back_populates="answers")

    # Establish a many-to-one relationship between Exam and Answer
    exam = relationship("Exam", back_populates="answers")

# Define association table for User and Exam
user_exam_association = Table(
    'user_exam_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('exam_id', Integer, ForeignKey('exams.id'))
)

# Define association table for User and Student
user_student_association = Table(
    'user_student_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('student_id', Integer, ForeignKey('students.id'))
)