import json
import pickle
import spacy

# Load intents
with open('trainingIntent.json') as file:
    data = json.load(file)

# Load the models and encoders
with open('intent_models-tp-v1.pkl', 'rb') as f:
    model_tag, le_tag, model_function, le_function, vectorizer = pickle.load(f)

# Initialize spacy
nlp = spacy.load('en_core_web_sm')

# Preprocess text: Lemmatization and lowercasing
def preprocess_text(text):
    return ' '.join([token.lemma_.lower() for token in nlp(text)])

def predict_intent(text):
    processed_text = preprocess_text(text)
    X_new = vectorizer.transform([processed_text])

    # Predict tag and function
    tag_prediction = le_tag.inverse_transform(model_tag.predict(X_new))[0]
    function_prediction = le_function.inverse_transform(model_function.predict(X_new))[0]

    # Find response for the predicted tag
    response = next((intent.get('responses', ["No response available"]) for intent in data['intents'] if intent['tag'] == tag_prediction), ["No response available"])[0]
    #function_prediction = next((intent.get('function', ["No response available"]) for intent in data['intents'] if intent['tag'] == tag_prediction), ["No response available"])

    return tag_prediction, function_prediction, response

# Function to process a command
def process_command(command):
    tag, function, response = predict_intent(command)
    print(f"Tag: {tag}, Function: {function}, Response: {response}")
    return response

# Example usage
if __name__ == "__main__":
    while True:
        user_input = input("enter : ")
        print(process_command(user_input))
