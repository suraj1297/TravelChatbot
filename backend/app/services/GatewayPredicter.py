from openai import OpenAI
import os
import json

class Predict:
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        self.messages = [
            {"role": "system", "content": "Jaarus is chatbot who helps booking flights and holidays"}
            ]
        
    def predict(self, sent):
        
        self.messages.append({"role": "user", "content": sent["input_data"]})
        
        completion = self.client.chat.completions.create(
            model= "ft:gpt-3.5-turbo-0613:personal:jaarusconvernewt2:8NosqS83",
			messages=self.messages,
			temperature=1.02,
			max_tokens=2048,
			top_p=1,
			frequency_penalty=0,
			presence_penalty=0
   		)
        
        response = completion.choices[0].message.content
        
        self.add_train_data([{"role": "user", "content": sent["input_data"]}, {"role": "assistant", "content": response}])
        
        self.messages.append({"role": "assistant", "content": response})
        
        return response
    
    def add_train_data(self, data):
        train_data = []
        with open("train_data.json", "r") as f:
            file_data = json.load(f)
            if file_data:
                train_data.extend(file_data)
                train_data.extend(data)
            else:
                train_data.extend(data)
        
        with open("train_data.json", "w") as f:
            json.dump(train_data, f, indent=4)
        