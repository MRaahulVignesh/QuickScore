from sqlalchemy.orm import Session
from sqlalchemy import exc

from backend.utils.db_conn import conn  
from backend.utils.errors import DatabaseError, DuplicateError, NotFoundError
from backend.models.models import StudentModel, AnswerModel

class StudentDao:
    def __init__(self):
        self.db = conn.get_db()

    # Create a new user
    def create_student(self, name: str, roll_no: str, email: str, user_id: int):
        try:
            student = StudentModel(name=name, roll_no=roll_no, email=email, user_id=user_id)
            self.db.add(student)
            self.db.commit()
            self.db.refresh(student)
        except exc.IntegrityError as error:
            print(error)
            raise DuplicateError("Similar Record already exists!")
        except Exception as error:
            print(error)
            raise DatabaseError("DB operation Failed: Create_Student")
        finally:
            self.db.close()
        return student

    # Retrieve a student by ID
    def get_student_by_id(self, id: int):
        try:
            student = self.db.query(StudentModel).filter(StudentModel.id == id).first()
            if student is None:
                raise NotFoundError("Student doesnot exist!")
        except Exception as error:
            print(error)
            raise DatabaseError("DB operation Failed: Get_Student_By_Id")
        return student

    # Retrieve a student by email
    def get_students_by_user_id(self, user_id: str):
        try:
            students = self.db.query(StudentModel).filter(StudentModel.user_id == user_id).all()
        except Exception as error:
            raise DatabaseError("DB operation Failed: Get_Student_By_User_Id")
        return students


    def delete_student(self, id: int):
        try:
            with self.db.begin() as transaction:
                student = self.db.query(StudentModel).filter(StudentModel.id == id).first()
                if student is None:
                    transaction.rollback()
                    raise NotFoundError("Student doesnot exist!")
                self.db.query(AnswerModel).filter(AnswerModel.student_id == student.id).delete()
                self.db.delete(student)
                transaction.commit()
        except NotFoundError as error:
            raise error
        except Exception as error:
            print(error)
            transaction.rollback()
            raise DatabaseError("DB operation Failed: Delete_Student")
        finally:
            self.db.close()
        return True
