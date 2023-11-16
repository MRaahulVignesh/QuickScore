import jwt
import datetime

from backend.utils.errors import NotFoundError, AuthenticationError
from backend.dao.answer_dao import AnswerDao
from backend.schemas.answer_schema import AnswerResponse, CreateAnswer
from backend.config.config import config
from backend.rag_models.question_splitter import QuestionSplitter

class AnswerCore:

    def __init__(self):
        self.answer_dao = AnswerDao()

    def create_answer(self, input: CreateAnswer, answer_pdf):
        
        # parsing the pdf 
        if answer_pdf == "":
            raise BadRequestError("Could not parse the pdf")
        qs = QuestionSplitter()
        json_answer_pdf = qs.splitter(answer_pdf)
        
        # send the json_answer_pdf and json_answer_key to the model
        
        
        #calculate the score
        score = 0.0
        
        # inserting the result
        answer_result = self.answer_dao.create_answer(exam_id=input.exam_id, student_id=input.student_id, score=score)
        answer, student = self.__extract_answer_and_student(answer_result)
        tmp = self.__create_answer_response(answer, student)
        answer = AnswerResponse.model_validate(tmp).model_dump(mode="json")
        return answer

    def get_answer_by_id(self, id: int):
        answer_result = self.answer_dao.get_answer_by_id(id)
        answer, student = self.__extract_answer_and_student(answer_result)
        tmp = self.__create_answer_response(answer, student)
        answer = AnswerResponse.model_validate(tmp).model_dump(mode="json")
        return answer

    def get_answers_by_exam_id(self, exam_id: int):
        answers = self.answer_dao.get_answers_by_exam_id(exam_id)
        new_answers = []
        for answer_result in answers:
            answer, student = self.__extract_answer_and_student(answer_result)
            tmp = self.__create_answer_response(answer, student)
            validated_answer = AnswerResponse.model_validate(tmp).model_dump(mode="json")
            new_answers.append(validated_answer)
        return new_answers

    def delete_answer(self, id: int):
        self.answer_dao.delete_answer(id)
        return True
    
    def __create_answer_response(self, answer, student):
        result = {}
        result["id"] = answer["id"]
        result["student_name"] = student["name"]
        result["student_roll_no"] = student["roll_no"]
        result["score"] = answer["score"]
        return result
    
    def __extract_answer_and_student(self, input):
        student = input[0].__dict__
        answer = input[1].__dict__
        return answer, student
