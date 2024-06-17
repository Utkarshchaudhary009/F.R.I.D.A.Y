import joblib

# Load model from file
model = joblib.load('gbm_model.pkl')

# Example usage:
query = "Captain America"
prediction = model.predict([query])
print("Predicted site:", prediction[0])