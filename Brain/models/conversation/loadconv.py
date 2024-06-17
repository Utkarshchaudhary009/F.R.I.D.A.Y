import pickle
import random
import json

# Load the model from the .pkl file
with open('query_type_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Load the responses from the JSON file
with open('./conversation.json', 'r') as f:
    data = json.load(f)

print("Model and data loaded successfully.")

# Function to get a response for a given query
def get_response(query):
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
# Test the function with sample queries
queries = [
    "hello jarvis",
    "what's the time alexa",
    "tell me a joke siri",
    "who created you",
    "how are you doing today?",
    "i am joining a new hobbi",
    "love me"
]

# Iterate through the queries and print the responses
for query in queries:
    response = get_response(query)
    print("Query:", query)
    print("Response:", response)
    print()
