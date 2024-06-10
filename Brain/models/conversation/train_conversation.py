import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import pickle
import json

# Load the responses from the JSON file
with open('./conversation.json', 'r') as f:
    data = json.load(f)

# Prepare the dataset
data_list = []
for key, value in data["responses"].items():
    for _ in value:  # Repeat the query for each response to balance the dataset
        data_list.append((key, key))

df = pd.DataFrame(data_list, columns=['query', 'response_type'])

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(df['query'], df['response_type'], test_size=0.2, random_state=42)

# Create a pipeline that includes TF-IDF vectorization and Naive Bayes classifier
model = make_pipeline(TfidfVectorizer(), MultinomialNB())

# Train the model
model.fit(X_train, y_train)

# Save the model to a .pkl file
with open('query_type_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model saved successfully as query_type_model.pkl.")
