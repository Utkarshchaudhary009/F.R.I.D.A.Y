import numpy as np
import librosa
import pickle

# Define the maximum length of the feature vector
MAX_FEATURE_LENGTH = 400

def extract_features(audio_path):
    y, sr = librosa.load(audio_path)
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
    zero_crossing_rate = librosa.feature.zero_crossing_rate(y=y)[0]
    mfcc = librosa.feature.mfcc(y=y, sr=sr).flatten()
    features = np.hstack([spectral_centroid, spectral_bandwidth, zero_crossing_rate, mfcc])
    
    # Ensure the feature vector has a fixed length
    if len(features) > MAX_FEATURE_LENGTH:
        features = features[:MAX_FEATURE_LENGTH]
    else:
        features = np.pad(features, (0, MAX_FEATURE_LENGTH - len(features)), 'constant')
        
    return features

# Load the trained model
model_filename = './command_music_classifier.pkl'
with open(model_filename, 'rb') as file:
    classifier = pickle.load(file)

# Example usage: classify a new audio sample
# audio_path = './Sound/commond/bluetooth_15.wav'
# audio_path = './Sound/music/segment_115.mp3'
audio_path = './output.wav'
features = extract_features(audio_path)
prediction = classifier.predict([features])

if prediction == 1:
    print("Command detected")
else:
    print("Background music detected")
