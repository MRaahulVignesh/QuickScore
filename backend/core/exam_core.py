import jwt
import datetime
import json
from backend.utils.errors import NotFoundError, AuthenticationError, InternalServerError
from backend.dao.exam_dao import ExamDao
from backend.schemas.exam_schema import ExamResponse
from backend.config.config import config
from backend.rag_models.question_splitter import QuestionSplitter


class ExamCore:

    def __init__(self):
        self.exam_dao = ExamDao()

    # Create a new user
    def create_exam(self, input: ExamResponse, answer_key: str = ""):
        if answer_key != "":
            qs = QuestionSplitter()
            json_answer_key = qs.splitter(answer_key)
            print(json_answer_key)
            if not self.__is_valid_json(str(json_answer_key)):
                raise InternalServerError("Error in splitting the answer key!")
            exam = self.exam_dao.create_exam(name= input.name, conducted_date=input.conducted_date, description=input.description, total_marks=input.total_marks, user_id=input.user_id, answer_key=answer_key)
        else:
            exam = self.exam_dao.create_exam(name= input.name, conducted_date=input.conducted_date, description=input.description, total_marks=input.total_marks, user_id=input.user_id)
        exam = ExamResponse.model_validate(exam).model_dump(mode="json")
        return exam

    # Retrieve a user by ID
    def get_exam_by_id(self, id: int):
        exam = self.exam_dao.get_exam_by_id(id)
        if exam is None:
            raise NotFoundError("Exam doesnot exist!")
        exam = ExamResponse.model_validate(exam).model_dump(mode="json")
        return exam

    # Retrieve a user by email
    def get_exams_by_user_id(self, user_id: int):
        print("hello")
        exams = self.exam_dao.get_exams_by_user_id(user_id)
        new_exams = []
        for exam in exams:
            tmp = ExamResponse.model_validate(exam).model_dump(mode="json")
            new_exams.append(tmp)
        return new_exams

    # Delete a user
    def delete_exam(self, id: int):
        self.exam_dao.delete_exam(id)
        return True

    def __is_valid_json(self, input_string):
        try:
            json.loads(input_string)
            return True
        except ValueError as error:
            print(error)
            return False