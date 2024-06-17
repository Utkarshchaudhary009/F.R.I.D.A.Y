import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import joblib

# Function to load the CNN model
def load_model(model_path='emotion_classifier_cnn.joblib'):
    # Load the model using joblib
    model = joblib.load(model_path)
    return model

# Function to preprocess text input
def preprocess_text(text, tokenizer, max_len):
    # Tokenize and pad the text
    sequences = tokenizer.texts_to_sequences([text])
    padded_sequences = pad_sequences(sequences, maxlen=max_len)
    return padded_sequences

# Function to predict emotion from user input
def predict_emotion(model, text, tokenizer, max_len):
    # Preprocess the text
    processed_text = preprocess_text(text, tokenizer, max_len)
    # Predict the emotion
    prediction = model.predict(processed_text)
    # Assuming binary classification, determine emotion based on threshold (e.g., 0.5)
    if prediction > 0.5:
        return "Positive"
    else:
        return "Negative"

# Main function to load model, preprocess text, and predict emotions
if __name__ == "__main__":
    # Load the CNN model
    model_path = 'emotion_classifier_cnn.joblib'
    model = load_model(model_path)
    
    # Load tokenizer and max_len used during training
    # Note: These should be saved during training for consistent preprocessing
    tokenizer = Tokenizer(num_words=1000)  # Adjust num_words based on training
    max_len = 100  # Adjust max_len based on training
    
    # Test the model with user input in a while loop
    print("Enter text to analyze (type 'exit' to quit):")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        emotion = predict_emotion(model, user_input, tokenizer, max_len)
        print(f"Predicted emotion: {emotion}")
