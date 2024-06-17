import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
import joblib
import os

os.remove("./gbm_model.pkl")

# Load dataset
data = pd.read_json('./querysite.json')

# Split data into features and target
X = data['querysite']
y = data['label']

# Define pipeline
model = make_pipeline(TfidfVectorizer(), GradientBoostingClassifier())

# Train model
model.fit(X, y)

# Save model to file
joblib.dump(model, 'gbm_model.pkl')