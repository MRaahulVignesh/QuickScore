# Import the Cohere client
import cohere
import re
import json
from backend.config.config import config

class QuestionSplitter:
    def __init__(self):
        self.api_key = config.COHERE_API_KEY
        print(self.api_key)
        # Initialize the Cohere client in the constructor
        self.co = cohere.Client(self.api_key)

    # Make sure to include 'self' as the first parameter in instance methods
    def splitter(self, text):
        prompt = f"""
            Please examine the given text in triple backticks and extract information for creating a JSON-formatted output. 
            The text may present in diverse formats, including but not limited to question-answer pairs, answers only, numbered questions with answers, or questions labeled in different ways 
            (like 'Q1:', '1. Question:', etc.) followed by answers. Regardless of the format, format the output with a number, the identified question (if any, otherwise leave it empty), and the corresponding answer. 
            For example, if the text includes 'Q1: What is your name? I am Helloveer. 1. Question: What is your name? I am Helloveer', adapt to these formats 
            and output something like: [{{'no': 1, 'question': 'What is your name?', 'answer': 'I am Helloveer'}}, {{'no': 2, 'question': 'What is your name?', 'answer': 'I am Helloveer'}}]. Be flexible and adapt to various formats of questions and answers as they appear in the text."
            Ensure to maintain single quote in the output json format for both keys and values.
            ```
             {text}
            ```
            """
        response = self.co.generate(
            model='command',
            prompt=prompt,
            max_tokens=1000,
            temperature=1.1,
            k=10,
            stop_sequences=[],
            return_likelihoods='NONE'
        )
        # Access the 'generations' key in the response

        print(response.generations[0].text)

        matches = re.findall(r'```json([\s\S]+?)```', response.generations[0].text)

        if matches:
            extracted_content = matches[0].strip()
            pre_json = extracted_content
            json_data = json.loads(pre_json)
            return json_data

        else:
            return json.loads("\{Not proper format\}")
        

# Usage example
if __name__ == "__main__":
    # Replace 'YOUR_API_KEY' with your actual API key
    api_key = 'ivWV8ybExfUclVP8Nj8X71jziG0YTYFjHlR8CjJs'
    key_splitter = AnswerKeySplitter(api_key)
    
    # Replace "Your input text goes here." with your actual input text
    input_text = "1)What is the unit of force in the SI system?\nThe unit of force in the SI system is the Newton (N).\n\n2)What does the law of conservation of energy state?\nThe law of conservation of energy states that energy cannot be created or destroyed, only transformed from one form to another.\n\n3)What is acceleration?\nAcceleration is the rate of change of velocity of an object with respect to time.\n\n4)How is weight different from mass?\nWeight is the force exerted by gravity on an object and depends on the object's mass and the gravitational field strength. Mass is the amount of matter in an object and is constant regardless of location.\n\n5)What is the formula for calculating speed?\nThe formula for speed is distance divided by time (Speed = Distance / Time).\n\n6)Define potential energy.\nPotential energy is the energy held by an object because of its position relative to other objects, stresses within itself, its electric charge, or other factors.\n\n7)What is the principle of moments?\nThe principle of moments states that when an object is in equilibrium, the sum of the clockwise moments about any point is equal to the sum of the anticlockwise moments about that same point.\n\n8)What is the difference between a scalar and a vector quantity?\nA scalar quantity has magnitude only, while a vector quantity has both magnitude and direction.\n\n9)What is meant by the frequency of a wave?\nThe frequency of a wave refers to the number of complete cycles of the wave that pass a point in a given period of time, typically measured in hertz (Hz).\n\n10)What is the principle of Archimedes?\nThe principle of Archimedes states that a body submerged in a fluid is buoyed up by a force equal to the weight of the fluid displaced by the body.\n\n."

    data = key_splitter.splitter(input_text)

    print(type(data))
    print(data)

