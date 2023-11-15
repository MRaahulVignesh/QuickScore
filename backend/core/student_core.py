import jwt
import datetime

from backend.utils.errors import NotFoundError, AuthenticationError
from backend.dao.student_dao import StudentDao
from backend.schemas.student_schema import StudentResponse, CreateStudent
from backend.config.config import config

class StudentCore:

    def __init__(self):
        self.student_dao = StudentDao()

    # Create a new student
    def create_student(self, input: CreateStudent):
        student = self.student_dao.create_student(name= input.name, roll_no= input.roll_no, email= input.email, user_id=input.user_id)
        student = StudentResponse.model_validate(student).model_dump(mode="json")
        return student

    # Retrieve a student by id
    def get_student_by_id(self, id: int):
        student = self.student_dao.get_student_by_id(id)
        student = StudentResponse.model_validate(student).model_dump(mode="json")
        return student

    # Retrieve a student by user_id
    def get_students_by_user_id(self, user_id: int):
        students = self.student_dao.get_students_by_user_id(user_id)
        new_students = []
        for student in students:
            tmp = StudentResponse.model_validate(student).model_dump(mode="json")
            new_students.append(tmp)
        return new_students

    # Delete a student
    def delete_student(self, id: int):
        print("hello")
        self.student_dao.delete_student(id)
        return True