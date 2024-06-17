import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
import joblib
import os
import json
import pygame

# Step 1: Load and preprocess data
data = []
input_dir = './input'

# Read all JSON files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.json'):
        print(filename)
        filepath = os.path.join(input_dir, filename)
        with open(filepath, 'r') as f:
            json_list = json.load(f)
            for json_data in json_list:
                data.append(json_data)

# Create a DataFrame from the loaded data
df = pd.DataFrame(data)

# Debugging: Print the first few rows of the DataFrame
print(df.head())

# Debugging: Print the column names
print(df.columns)

# Step 2: Split data into features (X) and labels (y)
# Ensure that the column names are correct
if 'common' not in df.columns or 'emotion' not in df.columns:
    raise KeyError("Expected columns 'common' and 'emotion' not found in the DataFrame")

X = df['common']  # Assuming 'common' contains the text snippets
y = df['emotion']  # Assuming 'emotion' contains the emotion labels

# Step 3: Create a pipeline with TfidfVectorizer and GradientBoostingClassifier
pipeline = make_pipeline(
    TfidfVectorizer(max_features=2000),  # Adjust max_features as needed
    GradientBoostingClassifier()
)

# Step 4: Train the model
pipeline.fit(X, y)

# Step 5: Save the trained model using joblib
joblib.dump(pipeline, 'emotion_classifier-best.joblib')
def play_audio():
    pygame.init()
    sound = pygame.mixer.Sound("../../models/Sound/music/Tu hai kahan.mp3")
    sound.play()
    while True:
        text=input("text: ")
        if text != "":
            sound.pause()
            pygame.quit()  # Quit pygame to release resources
        else :
            pass
play_audio()
print("Training and saving the model complete.")
