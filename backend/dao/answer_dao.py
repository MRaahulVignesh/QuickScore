from sqlalchemy.orm import Session, aliased
from sqlalchemy import exc

from backend.utils.db_conn import postgres_conn  
from backend.utils.errors import DatabaseError, DuplicateError, NotFoundError
from backend.models.models import AnswerModel, StudentModel

class AnswerDao:
    def __init__(self):
        self.db = postgres_conn.get_db()

    def create_answer(self, student_id: int, exam_id: int, score: float, confidence: float, filename: str, evaluation_details):
        try:
            answer = AnswerModel(score=score, student_id=student_id, exam_id=exam_id, confidence=confidence, evaluation_details=evaluation_details, file_name=filename)
            self.db.add(answer)
            self.db.commit()
            self.db.refresh(answer)
            result = self.get_answer_by_id(answer.id)
        except exc.IntegrityError as error:
            print(error)
            raise DuplicateError("Similar Record already exists!")
        except Exception as error:
            print(error)
            raise DatabaseError("DB operation Failed: Create_Answer")
        finally:
            self.db.close()
        return result

    def get_answer_by_id(self, id: int):
        try:
            # answer = self.db.query(AnswerModel).filter(AnswerModel.id == id).first()
            filtered_answer_subquery = self.db.query(AnswerModel).filter(AnswerModel.id == id).subquery()
            filtered_answer = aliased(AnswerModel, filtered_answer_subquery)
            result = self.db.query(StudentModel, filtered_answer).join(filtered_answer, StudentModel.id == filtered_answer.student_id).first()
            if result is None:
                raise NotFoundError("Answer doesnot exist!")
        except Exception as error:
            print(error)
            raise DatabaseError("DB operation Failed: Get_Answer_By_Id")
        return result

    def get_answers_by_exam_id(self, exam_id: str):
        try:
            filtered_answers_subquery = self.db.query(AnswerModel).filter(AnswerModel.exam_id == exam_id).subquery()
            filtered_answers = aliased(AnswerModel, filtered_answers_subquery)
            results = self.db.query(StudentModel, filtered_answers).join(filtered_answers, StudentModel.id == filtered_answers.student_id).all()
        except Exception as error:
            print(error)
            raise DatabaseError("DB operation Failed: Get_Answers_By_User_Id")
        return results


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
