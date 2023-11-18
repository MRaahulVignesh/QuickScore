import datetime

from backend.utils.errors import BadRequestError, InternalServerError, NotFoundError, AuthenticationError
from backend.dao.answer_dao import AnswerDao
from backend.dao.exam_dao import ExamDao
from backend.schemas.answer_schema import AnswerResponse, CreateAnswer, AnswerIndividualResponse
from backend.config.config import config
from backend.rag_models.question_splitter import QuestionSplitter
from backend.rag_models.grader import GraderCohere

class AnswerCore:

    def __init__(self):
        self.answer_dao = AnswerDao()
        self.exam_dao = ExamDao()
    

    def create_answer(self, input: CreateAnswer, answer_pdf, filename):
        
        # send the json_answer_pdf and json_answer_key to the model
        exam_context_details = self.exam_dao.get_exam_by_id(input.exam_id)
        if exam_context_details[0] is not None:
            exam_details = exam_context_details[0].__dict__
        else:
            raise InternalServerError("Provided Exam Details not Present")
        
        if exam_context_details[1] is not None:
            context_details = exam_context_details[1].__dict__
            context_key = context_details["context_key"]
        else:
            context_key = None
        
        # parsing the pdf 
        if answer_pdf == "":
            raise BadRequestError("Could not parse the pdf")
        qs = QuestionSplitter()
        
        json_answer_pdf = qs.splitter(answer_pdf)
        json_answer_key = exam_details["answer_key"]
        
        sorted_student_answer = self.__sort_json_by_no(json_answer_pdf)
        sorted_answer_key = self.__sort_json_by_no(json_answer_key)

        
        # #list json
        j,k=0,0
        json_answer_list = []
        for i in range(max(len(sorted_student_answer), len(sorted_answer_key))):
            temp={}
            if sorted_student_answer[j]["no"] == sorted_answer_key[k]["no"]:
                temp["question"] = sorted_answer_key[k]["question"]
                temp["student_answer"] = sorted_student_answer[j]["answer"]
                temp["answer_key"] = sorted_answer_key[k]["answer"]
                j+=1
                k+=1
            elif sorted_student_answer[j]["no"] > sorted_answer_key[k]["no"]:
                temp["question"] = sorted_answer_key[k]["question"]
                temp["student_answer"] = ""
                temp["answer_key"] = sorted_answer_key[k]["asnwer"]      
                k+=1
            else:
                raise InternalServerError("Error in Answer key")   
            json_answer_list.append(temp)                        
        
        cohere_grader = GraderCohere(context_key)
        evaluation_result, total_score = cohere_grader.grade(json_answer_list)

        #calculate the score
        score = total_score
        
        #calculate the confidence
        confidence = 0.0
        
        # inserting the result
        answer_result = self.answer_dao.create_answer(exam_id=input.exam_id, student_id=input.student_id, score=score, confidence=confidence, evaluation_details=evaluation_result, filename=filename)
        answer, student = self.__extract_answer_and_student(answer_result)
        tmp = self.__create_answer_response(answer, student, exam_details)
        # answer = AnswerResponse.model_validate(tmp).model_dump(mode="json")
        return tmp

    def get_answer_by_id(self, id: int):
        answer_result = self.answer_dao.get_answer_by_id(id)
        answer, student = self.__extract_answer_and_student(answer_result)
        exam = self.exam_dao.get_exam_by_id(answer["exam_id"])
        exam = exam[0].__dict__
        tmp = self.__create_individual_answer_response(answer, student, exam)
        return tmp

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
        result["file_name"] = answer["file_name"]
        return result

    def __create_individual_answer_response(self, answer, student, exam):
        result = {}
        result["id"] = answer["id"]
        result["student_name"] = student["name"]
        result["student_roll_no"] = student["roll_no"]
        result["score"] = answer["score"]
        result["confidence"] = answer["confidence"]
        result["file_name"] = answer["file_name"]
        result["evaluation_details"] = answer["evaluation_details"]
        result["max_exam_score"] = exam["total_marks"]
        return result
    
    def __extract_answer_and_student(self, input):
        student = input[0].__dict__
        answer = input[1].__dict__
        return answer, student
    
    def __sort_json_by_no(self, json_data):
        # Sort the list of dictionaries by the value of the "no" key
        return sorted(json_data, key=lambda x: x['no'])
