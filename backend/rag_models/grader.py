import os
import weaviate
import json
from langchain.llms import Cohere
from langchain.embeddings import CohereEmbeddings
from backend.config.config import config
import getpass
from langchain.embeddings import CohereEmbeddings
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import Weaviate
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import TextLoader
from langchain.retrievers.document_compressors import CohereRerank
from langchain.chains import RetrievalQA
import cohere


class GraderCohere:
    def __init__(self, class_name):

        cohere_api_key = config.COHERE_API_KEY
        weaviate_api_key = config.WEAVIATE_API_KEY
        weaviate_url = config.WEAVIATE_URL

        self.class_name = class_name
        self.no_of_k = 10

        self.client=weaviate.Client(
            url=weaviate_url,
            auth_client_secret=weaviate.AuthApiKey(api_key=weaviate_api_key),

            additional_headers={
                "X-Cohere-Api-Key": cohere_api_key,
            }
        )
        if class_name is not None:
            _weaviate = Weaviate(self.client, self.class_name, "text").as_retriever(
                search_kwargs={"k": self.no_of_k}
            )
            self.chain = RetrievalQA.from_chain_type(
                llm=Cohere(cohere_api_key = cohere_api_key,temperature=0), retriever=_weaviate
            )
        else:
            self.chain = cohere.Client(cohere_api_key)

    def grade(self, list_json):
        
        print(list_json)

        graded = []
        print("hello12345")
        if self.class_name is not None:
            for item in list_json:
                
                p1 = f""" 
                    ```
                    Question: 
                        {item['question']}
                    Answer Key: 
                        {item['answer_key']}
                    Student Answer: 
                        {item['student_answer']}
                    ```
                    
                    Below is the Task to be performed
                        Refer to the text inside triple backtickets that contain Question, Answer Key and Student Answer. 
                        Grade leniently the Student Answer out of 5 marks, with 5 being maximum mark awarded for a correct answer and 0 being the minimum mark awarded for a completely wrong answer. 
                        Partial marks can also be awarded if the answer is partially correct. 
                        Mention the mark and explain with proper justification for awarding or not awarding marks.
                        Prompt: Can you respond only by printing in the following json output format which could be converted into json without any errors:
                        
                        output format:
                            {{"Marks": <insert awarded marks after evaluation>,
                             "Justification": <insert justification>,
                            }}
                """ 
                print(p1)
                # p1 = "Question: "+item['question']+"\nAnswer Key: "+item['answer_key']+"\nStudent Answer: "+item['student_answer']+"\n Grade leniently the Student Answer out of 5 marks, with 5 being maximum mark awarded for a correct answer and 0 being the minimum mark awarded for a completely wrong answer. Partial marks can also be awarded if the answer is partially correct. Mention the mark and explain with proper justification for awarding or not awarding marks.\n Prompt: Can you respond only by printing in the following json format which could be converted into json without any errors:\n  \n{\"Marks\": ,\n\"Justification\": ,\n}\n \n"
                response = self.chain({"query": p1})['result']
                print(response)
                resp = json.loads(response)
                graded.append(resp)
        else:
            for item in list_json:
                p1 = f""" 
                    ```
                    Question: 
                        {item['question']}
                    Answer Key: 
                        {item['answer_key']}
                    Student Answer: 
                        {item['student_answer']}
                    ```
                    
                    Below is the Task to be performed
                        Refer to the text inside triple backtickets that contain Question, Answer Key and Student Answer. 
                        Grade leniently the Student Answer out of 5 marks, with 5 being maximum mark awarded for a correct answer and 0 being the minimum mark awarded for a completely wrong answer. 
                        Partial marks can also be awarded if the answer is partially correct. 
                        Mention the mark and explain with proper justification for awarding or not awarding marks.
                        Prompt: Can you respond only by printing in the following json format which could be converted into json without any errors:
                        {{\"Marks\": ,\n\"Justification\": ,\n}}
                """ 
                print(p1)
                # p1 = "Question: "+item['question']+"\nAnswer Key: "+item['answer_key']+"\nStudent Answer: "+item['student_answer']+"\n Grade leniently the Student Answer out of 5 marks, with 5 being maximum mark awarded for a correct answer and 0 being the minimum mark awarded for a completely wrong answer. Partial marks can also be awarded if the answer is partially correct. Mention the mark and explain with proper justification for awarding or not awarding marks.\n Prompt: Can you respond only by printing in the following json format which could be converted into json without any errors:\n  \n{\"Marks\": ,\n\"Justification\": ,\n}\n \n"
                response = self.chain.generate(
                    model='command',
                    prompt=p1,
                    max_tokens=2000,
                    temperature=0,
                    k=10,
                    stop_sequences=[],
                    return_likelihoods='NONE')
            
                resp = json.loads(response.generations[0].text)
                graded.append(resp)

        grad_complete = []
        total_marks = 0
        for i in range(len(list_json)):
            temp = {}
            temp['no']=i+1
            temp['question'] = list_json[i]['question']
            temp['answer_key'] = list_json[i]['answer_key']
            temp['student_answer'] = list_json[i]['student_answer']
            temp['marks'] = graded[i]['Marks']
            temp['justification'] = graded[i]['Justification']
            total_marks += float(graded[i]['Marks'])

            grad_complete.append(temp)

        return grad_complete, total_marks