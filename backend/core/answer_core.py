import jwt
import datetime

from backend.utils.errors import NotFoundError, AuthenticationError
from backend.dao.answer_dao import AnswerDao
from backend.dao.exam_dao import ExamDao
from backend.schemas.answer_schema import AnswerResponse, CreateAnswer
from backend.config.config import config
from backend.rag_models.question_splitter import QuestionSplitter
from backend.rag_models.grader import GraderCohere

class AnswerCore:

    def __init__(self):
        self.answer_dao = AnswerDao()
        self.exam_dao = ExamDao()
    

    def create_answer(self, input: CreateAnswer, answer_pdf):
        
        # send the json_answer_pdf and json_answer_key to the model
        exam_context_details = self.exam_dao.get_exam_by_id(input.exam_id)
        exam_details = exam_context_details[0].__dict__
        context_details = exam_context_details[1].__dict__
        
        context_key = context_details["context_key"]
        
        print(exam_details, context_details)
        
        # parsing the pdf 
        if answer_pdf == "":
            raise BadRequestError("Could not parse the pdf")
        qs = QuestionSplitter()
        
        json_answer_pdf = qs.splitter(answer_pdf)
        json_answer_key = exam_details["answer_key"]
        
        # #list json
        # j,k=0,0
        # for i in range(max(len(json_answer_pdf), len(json_answer_key))):
        #     q_no_j = 
        #     q_no_k = json_answer_key[k]
        #     if json_answer_pdf[j]["no"] == json_answer_key[k]["no"]:
                
            

        
        # print(context_key)
        # cohere_grader = GraderCohere(context_key)
        # cohere_grader.grade()

        
        #calculate the score
        score = 0.0
        
        #calculate the confidence
        confidence = 0.0
        
        # inserting the result
        answer_result = self.answer_dao.create_answer(exam_id=input.exam_id, student_id=input.student_id, score=score, confidence=confidence)
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
        result["confidence"] = answer["confidence"]
        return result
    
    def __extract_answer_and_student(self, input):
        student = input[0].__dict__
        answer = input[1].__dict__
        return answer, student
