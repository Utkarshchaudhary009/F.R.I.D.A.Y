import os
import sys
# Ensure the parent directory is in sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
import random
import pickle
import random
import json
import datetime
from datetime import datetime
import inflect

# Initialize inflect engine
p = inflect.engine()

# Function to convert a number to its written form
def number_to_words(number):
    return p.number_to_words(number).replace('-', ' ')

# Function to get current date, day, and time in written format
def get_written_date_time():
    now = datetime.now()
    
    # Get current date parts
    day = now.day
    month = now.strftime("%B")
    year = now.year

    # Get current time parts
    hour = now.hour
    minute = now.minute
    second = now.second

    # Convert each part to words
    written_day = number_to_words(day)
    written_year = number_to_words(year)
    written_hour = number_to_words(hour)
    written_minute = number_to_words(minute)
    written_second = number_to_words(second)

    # Construct the written date and time
    written_date = f"{written_day} {month} {written_year}"
    written_time = f"{written_hour} {written_minute} {written_second}"

    # Get current weekday
    weekday = now.strftime("%A")

    return {"Date": {written_date}, "Day": {weekday}, "Time": {written_time}}
# Load the model from the .pkl file
with open('f:\Friday\Brain/models/conversation/query_type_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Load the responses from the JSON file
with open('f:\Friday\Brain/models/conversation/conversation.json', 'r') as f:
    data = json.load(f)

# print("Model and data loaded successfully.")

# Function to get a response for a given query
    # RFM=Response from Model
def RFM(query):
    if "siri" in query:
        return random.choice(data["responses"]["hello siri"])
    elif "jarvis" in query:
        return random.choice(data["responses"]["hi jarvis"])
    elif "alexa" in query:
        return random.choice(data["responses"]["hey alexa"])
    elif "google" in query:
        return random.choice(data["responses"]["ok google"])
    else:
        predicted_query_type =model.predict([query])[0]
        if predicted_query_type in data["responses"]:
            timeData=get_written_date_time()
            print(timeData)
            res=random.choice(data["responses"][predicted_query_type])
            print(res)
            if "{date}" in res:
                return res.format(date=timeData["Date"])
            elif "{day}" in res:
                return res.format(day=timeData["Day"])
            elif "{time}" in res:
                return res.format(time=timeData["Time"])
            else:
                return res
        else:
            return "I'm not sure how to respond to that."



def get_response(user_input):
        user_input = user_input.lower()
        
        return {"response":RFM(user_input)}

# Example Usage
if __name__ == "__main__":
    # Example inputs
    inputs = [
        "love you friday",
        "friday",
        "friday how are you",
        "tell me a joke",
        "hello",
        "how are you",
        "what's your name",
        "good morning",
        "good night",
        "thank you",
    "hello jarvis",
    "what's the time alexa",
    "tell me a joke siri",
    "who created you",
    "how are you doing today?",
    "what can you do?",
    "tell me the time"
    ]
    # Get responses for example inputs
    for inp in inputs:
        print(f"User: {inp}")
        print(f"Friday: {get_response(inp)}\n")
