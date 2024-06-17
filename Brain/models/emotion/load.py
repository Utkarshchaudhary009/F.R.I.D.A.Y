import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
import joblib

def load_model(model_path='emotion_classifier.joblib'):
    return joblib.load(model_path)

# Predict emotion from user input
def predict_emotion(model, text):
    return model.predict([text])

# Main function to train, save, and test the model
if __name__ == "__main__":
    model_path = './emotion_classifier.joblib'
    # Load the model
    model = load_model(model_path)
    # Test the model with user input in a while loop
    print("Enter text to analyze (type 'exit' to quit):")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        emotion = predict_emotion(model, user_input)
        print(f"Predicted emotion: {emotion}")
