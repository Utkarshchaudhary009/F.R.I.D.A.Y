import json
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
import pickle

# Load language data from JSON file
LANGCODE_FILE = './langcode.json'

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    lang_names = [item['name'] for item in data]
    lang_codes = [item['code'] for item in data]
    return lang_names, lang_codes

# Training the model
def train_and_save_model(lang_names, lang_codes, model_file='language_code_model.pkl'):
    # Convert language names to feature vectors
    vectorizer = CountVectorizer()
    
    # Encode language codes as numerical labels
    label_encoder = LabelEncoder()
    
    # Create a pipeline
    model = Pipeline([
        ('vectorizer', vectorizer),
        ('classifier', MultinomialNB())
    ])
    
    
    # Fit the model
    X = lang_names
    y = label_encoder.fit_transform(lang_codes)
    model.fit(X, y)
    
    # Save the label encoder and the model to disk
    with open(model_file, 'wb') as f:
        pickle.dump((model, label_encoder), f)
    print(f"Model saved to {model_file}")

if __name__ == "__main__":
    lang_names, lang_codes = load_data(LANGCODE_FILE)
    train_and_save_model(lang_names, lang_codes)
