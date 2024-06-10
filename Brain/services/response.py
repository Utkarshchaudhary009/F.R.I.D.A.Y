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
            return random.choice(data["responses"][predicted_query_type])
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
    "what can you do?"
    ]
    # Get responses for example inputs
    for inp in inputs:
        print(f"User: {inp}")
        print(f"Friday: {get_response(inp)}\n")
