import jwt
import datetime

from backend.utils.errors import NotFoundError, AuthenticationError
from backend.dao.answer_dao import AnswerDao
from backend.schemas.answer_schema import AnswerResponse, CreateAnswer
from backend.config.config import config

class AnswerCore:

    def __init__(self):
        self.answer_dao = AnswerDao()

    def create_answer(self, input: CreateAnswer):
        answer = self.answer_dao.create_answer(exam_id=input.exam_id, student_id=input.student_id, score=input.score)
        answer = AnswerResponse.model_validate(answer).model_dump(mode="json")
        return answer

    def get_answer_by_id(self, id: int):
        answer = self.answer_dao.get_answer_by_id(id)
        answer = AnswerResponse.model_validate(answer).model_dump(mode="json")
        return answer

    def get_answers_by_exam_id(self, exam_id: int):
        answers = self.answer_dao.get_answers_by_exam_id(exam_id)
        new_answers = []
        for answer in answers:
            tmp = AnswerResponse.model_validate(answer).model_dump(mode="json")
            new_answers.append(tmp)
        return new_answers

    def delete_answer(self, id: int):
        self.answer_dao.delete_answer(id)
        return True
        
