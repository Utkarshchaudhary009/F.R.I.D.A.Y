import json
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import pickle
import os
# Load intents
with open('./trainingIntent.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Initialize spacy
nlp = spacy.load('en_core_web_sm')
# os.remove('./intent_models-TOF-v1.pkl')
# Extract patterns, tags, function names, and responses
patterns = []
tags = []
functions = []
responses = []

for intent in data['intents']:
    for pattern in intent['patterns']['NLPPattern']:
        patterns.append(pattern)
        tags.append(intent['tag'])
        functions.append(intent['function'])
        responses.append(intent.get('responses', []))

# Preprocess text: Lemmatization and lowercasing
def preprocess_text(text):
    return ' '.join([token.lemma_.lower() for token in nlp(text)])

patterns = [preprocess_text(pattern) for pattern in patterns]

# Convert text to features
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(patterns)

# Encode labels for tags and functions
le_tag = LabelEncoder()
y_tag = le_tag.fit_transform(tags)

le_function = LabelEncoder()
y_function = le_function.fit_transform(functions)

# Train SVM models for tags and functions
model_tag = SVC(kernel='linear', C=1, random_state=42)
model_tag.fit(X, y_tag)

model_function = SVC(kernel='linear', C=1, random_state=42)
model_function.fit(X, y_function)

# Save the models, vectorizer, and label encoders
with open('intent_models-TOF-v1.pkl', 'wb') as f:
    pickle.dump((model_tag, le_tag, model_function, le_function, vectorizer), f)

print("Models trained and saved successfully!")
