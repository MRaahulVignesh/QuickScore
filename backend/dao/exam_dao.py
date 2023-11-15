import datetime
from sqlalchemy.orm import Session
from sqlalchemy import exc

from backend.utils.db_conn import postgres_conn  
from backend.utils.errors import DatabaseError, DuplicateError, NotFoundError
from backend.models.models import ExamModel, AnswerModel

class ExamDao:
    def __init__(self):
        self.db = postgres_conn.get_db()

    # Create a new user
    def create_exam(self, name: str, conducted_date: datetime, description: str, total_marks: float, user_id: int):
        try:
            exam = ExamModel(name=name, conducted_date=conducted_date, description=description, total_marks=total_marks, user_id=user_id)
            self.db.add(exam)
            self.db.commit()
            self.db.refresh(exam)
        except exc.IntegrityError as error:
            print(error)
            raise DuplicateError("Similar Record already exists!")
        except Exception as error:
            print(error)
            raise DatabaseError("DB operation Failed: Create_Exam")
        finally:
            self.db.close()
        return exam

    # Retrieve a user by ID
    def get_exam_by_id(self, id: int):
        try:
            exam = self.db.query(ExamModel).filter(ExamModel.id == id).first()
            if exam is None:
                raise NotFoundError("Exam doesnot exist!")
        except Exception as error:
            print(error)
            raise DatabaseError("DB operation Failed: Get_Exam_By_Id")
        return exam

    def get_exams_by_user_id(self, user_id: int):
        try:
            exams = self.db.query(ExamModel).filter(ExamModel.user_id == user_id).all()
        except Exception as error:
            print(error)
            raise DatabaseError("DB operation Failed: Get_Exam_By_Id")
        return exams

    # Delete a exam
    def delete_exam(self, id: int):
        try:
            with self.db.begin() as transaction:
                exam = self.db.query(ExamModel).filter(ExamModel.id == id).first()
                if exam is None:
                    raise NotFoundError("Exam doesnot exist!")
                self.db.query(AnswerModel).filter(AnswerModel.exam_id == exam.id).delete()
                self.db.delete(exam)
                transaction.commit()
        except Exception as error:
            print(error)
            transaction.rollback()
            raise DatabaseError("DB operation Failed: Delete_Exam")
        finally:
            self.db.close()
        return True
