import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dense, Dropout
from sklearn.model_selection import train_test_split
import joblib

# Step 1: Load and preprocess data
data = []
input_dir = './input'

# Read all JSON files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.json'):
        filepath = os.path.join(input_dir, filename)
        with open(filepath, 'r') as f:
            json_list = json.load(f)
            for json_data in json_list:
                data.append(json_data)

# Convert data into lists of texts and labels
texts = [entry['common'] for entry in data]
labels = [entry['emotion'] for entry in data]

# Step 2: Tokenize texts and prepare sequences
max_words = 1000  # Maximum number of words to tokenize
max_len = 100  # Maximum length of each sequence

tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
X = pad_sequences(sequences, maxlen=max_len)
y = np.array(labels)

# Step 3: Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Build the CNN model
embedding_dim = 100  # Dimension of word embeddings
num_filters = 128  # Number of filters in Conv1D layer
kernel_size = 5  # Kernel size for Conv1D layer

model = Sequential([
    Embedding(max_words, embedding_dim, input_length=max_len),
    Conv1D(num_filters, kernel_size, activation='relu'),
    GlobalMaxPooling1D(),
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')  # Assuming binary classification (positive/negative emotion)
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Step 5: Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Step 6: Save the trained model using joblib (optional for Keras models, but can use for custom objects)
joblib.dump(model, 'emotion_classifier_cnn.joblib')

print("Training and saving the CNN model complete.")
