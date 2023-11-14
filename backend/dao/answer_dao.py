from sqlalchemy.orm import Session
from sqlalchemy import exc

from backend.utils.db_conn import postgres_conn  
from backend.utils.errors import DatabaseError, DuplicateError, NotFoundError
from backend.models.models import AnswerModel

class AnswerDao:
    def __init__(self):
        self.db = postgres_conn.get_db()

    def create_answer(self, student_id: int, exam_id: int, score: float):
        try:
            answer = AnswerModel(score=score, student_id=student_id, exam_id=exam_id)
            self.db.add(answer)
            self.db.commit()
            self.db.refresh(answer)
        except exc.IntegrityError as error:
            print(error)
            raise DuplicateError("Similar Record already exists!")
        except Exception as error:
            print(error)
            raise DatabaseError("DB operation Failed: Create_Student")
        finally:
            self.db.close()
        return answer

    def get_answer_by_id(self, id: int):
        try:
            answer = self.db.query(AnswerModel).filter(AnswerModel.id == id).first()
            if answer is None:
                raise NotFoundError("Answer doesnot exist!")
        except Exception as error:
            print(error)
            raise DatabaseError("DB operation Failed: Get_Answer_By_Id")
        return answer

    def get_answers_by_exam_id(self, exam_id: str):
        try:
            answers = self.db.query(AnswerModel).filter(AnswerModel.exam_id == exam_id).all()
        except Exception as error:
            raise DatabaseError("DB operation Failed: Get_Answers_By_User_Id")
        return answers


    def delete_answer(self, answer_id: int):
        try:
            answer = self.db.query(AnswerModel).filter(AnswerModel.id == answer_id).first()
            if answer is None:
                raise NotFoundError("Answer doesnot exist!")
            self.db.delete(answer)
            self.db.commit()
        except Exception as error:
            print(error)
            raise DatabaseError("DB operation Failed: Delete_Answer")
        return True
