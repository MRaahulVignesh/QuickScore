# Import the Cohere client
import cohere
import re
import json
from backend.config.config import config
from backend.utils.errors import ModelError

class QuestionSplitter:
    def __init__(self):

        self.api_key = config.COHERE_API_KEY
        # Initialize the Cohere client in the constructor
        self.co = cohere.Client(self.api_key)

    # Make sure to include 'self' as the first parameter in instance methods
    def splitter(self, text):

        prompt = f"""
            Please examine the given text in triple backticks and extract information for creating a JSON-formatted output. 
            The text may present in diverse formats, including but not limited to question-answer pairs, answers only, numbered questions with answers, or questions labeled in different ways 
            (like "Q1:", "1. Question:", etc.) followed by answers. Regardless of the format, 
            
            
            format the output with a number, the identified question (if any, otherwise leave it empty), and the corresponding answer. 
            For example, if the text includes 'Q1: What is your name? I am Helloveer. 1. Question: What is your name? I am Helloveer', adapt to these formats 
            and output something like: [{{"no": 1, "question": "What is your name?", "answer": "I am Helloveer"}}, {{"no": 2, "question": "What is your name?", "answer": "I am Helloveer"}}]. Be flexible and adapt to various formats of questions and answers as they appear in the text."
            Ensure to maintain double quote in the output json format for both keys and values.
            ```
             {text}
            ```
            """
            
        print(prompt)
            
        response = self.co.generate(
            model='command',
            prompt=prompt,
            max_tokens=1000,
            temperature=1.1,
            k=10,
            stop_sequences=[],
            return_likelihoods='NONE'
        )
        
        extracted_response = response.generations[0].text

        print(extracted_response)

        matches = re.findall(r'```json([\s\S]+?)```',extracted_response)

        if matches:
            extracted_content = matches[0].strip()
            pre_json = extracted_content
            print(pre_json)
            json_data = json.loads(pre_json)
            print(json_data)
            return json_data
        else:
            try:
                json_data = json.loads(extracted_response)
                print(json_data)
                return json_data
            except Exception as error:
                print(error)
                raise ModelError("Error in Parsing Json")
                
            raise ModelError("Error in Parsing Json")

