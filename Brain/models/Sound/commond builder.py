import json
import os
from gtts import gTTS

# Directory where the audio files will be saved
output_dir = 'Sound/commond'
os.makedirs(output_dir, exist_ok=True)

# Function to read JSON file
def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Function to convert text to audio and save
def text_to_audio(text, filename):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    print(f"Saved {filename}")

# Read the JSON data
file_path = '../intent/trainingIntent.json'
data = read_json(file_path)

# Extract NLP patterns and convert to audio
for intent in data['intents']:
    tag = intent['tag']
    patterns = intent['patterns']['NLPPattern']
    
    for idx, pattern in enumerate(patterns):
        filename = os.path.join(output_dir, f"{tag}_{idx+1}.wav")
        text_to_audio(pattern, filename)
