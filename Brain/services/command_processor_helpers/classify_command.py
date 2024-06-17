import re
import json
import pickle
import os
import sys
import spacy
import subprocess
from .extract_arguments import extract_arguments

# Ensure the parent directory is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from nlp_processing import NLPProcessor

class IntentClassifier:
    def __init__(self, intents_file, model_file):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        intents_file_path = os.path.join(current_directory, intents_file)
        model_file_path = os.path.join(current_directory, model_file)

        with open(intents_file_path, 'r', encoding='utf-8') as file:
            self.intents_data = json.load(file)

        with open(model_file_path, 'rb') as f:
            self.model_tag, self.le_tag, self.model_function, self.le_function, self.vectorizer = pickle.load(f)

        # Initialize spacy directly as in trymodel.py
        self.nlp = spacy.load('en_core_web_sm')
        
        # Initialize NLP processor
        self.nlp_processor = NLPProcessor()

    def preprocess(self, text):
        return ' '.join([token.lemma_.lower() for token in self.nlp(text)])

    def predict_intent(self, command):
        processed_txt = self.preprocess(command)
        X_new = self.vectorizer.transform([processed_txt])

        tag_prediction = self.le_tag.inverse_transform(self.model_tag.predict(X_new))[0]
        function_prediction = self.le_function.inverse_transform(self.model_function.predict(X_new))[0]

        response = next((intent.get('responses', ["No response available"]) for intent in self.intents_data['intents'] if intent['tag'] == tag_prediction))
        return tag_prediction, function_prediction, response

    def extract_arguments(self, command, intent_tag):
        command=command.replace("friday","").replace("friday,","").replace(" hey friday","").replace(" bro friday,","").replace("song",'').replace("Song",'')
        tokens = self.preprocess(command).split()
        pos_tags = self.nlp_processor.pos_tagging(tokens)
        entities = self.nlp_processor.ner(command)
        intent = next(intent for intent in self.intents_data['intents'] if intent["tag"] == intent_tag)
        arguments = extract_arguments(command, intent_tag, tokens, pos_tags, entities, self.intents_data['intents'])
        return arguments

def classify_command(command):
    classifier = IntentClassifier('f:\Friday\Brain/models/intent/trainingIntent.json', 'f:\Friday\Brain\models/intent/intent_models-TOF-v1.pkl')

    # Predict intent
    tag, function, response = classifier.predict_intent(command)
    print("Predicted Intent:", tag)
    print("Function:", function)
    print("Response:", response)
    if tag not in ["search_wolframalpha", "search_wikipedia", "response","movie_detail","play_song","book",'keymagic','translation','search_on_web','cricket']:
    # if tag not in ["search_wolframalpha", "search_wikipedia", "response","movie_detail"]:
        arguments = classifier.extract_arguments(command, tag)
        print("1234567890 : ", arguments)
    else:
        arguments = command
    
    print(function,arguments)
    return function, arguments

# Example usage
if __name__ == "__main__":
    while True:
        user_input = input("Enter command: ")
        function, arguments = classify_command(user_input)
        print("Function:", function)
        print("Arguments:", arguments)
