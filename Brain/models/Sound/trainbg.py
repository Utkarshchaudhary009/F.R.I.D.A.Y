import os
import numpy as np
import librosa
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

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

def load_data(data_dir):
    X, y = [], []
    for label, subdir in enumerate(['commond', 'music']):
        subdir_path = os.path.join(data_dir, subdir)
        for filename in os.listdir(subdir_path):
            file_path = os.path.join(subdir_path, filename)
            if filename.endswith('.wav') or filename.endswith('.mp4'):
                features = extract_features(file_path)
                X.append(features)
                y.append(label)
    return np.array(X), np.array(y)

# Load and process the data
data_dir = './Sound'
X, y = load_data(data_dir)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest classifier
classifier = RandomForestClassifier(n_estimators=100, random_state=42)
classifier.fit(X_train, y_train)

# Evaluate the model
y_pred = classifier.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

# Save the trained model
model_filename = 'command_music_classifier.pkl'
with open(model_filename, 'wb') as file:
    pickle.dump(classifier, file)
print(f"Model saved to {model_filename}")
