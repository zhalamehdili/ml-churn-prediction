import joblib
import numpy as np

# Load artifacts
model = joblib.load('models/model.pkl')
scaler = joblib.load('models/scaler.pkl')
feature_names = joblib.load('models/feature_names.pkl')
label_encoders = joblib.load('models/label_encoders.pkl')

print("Model and preprocessing artifacts loaded.")
print(f"Number of features: {len(feature_names)}")

# Build a dummy sample with the correct number of features
test_sample = np.zeros((1, len(feature_names)))

# Scale and predict
test_scaled = scaler.transform(test_sample)
prediction = model.predict(test_scaled)
proba = model.predict_proba(test_scaled)

print("\nDummy prediction made.")
print(f"Predicted class (0=No churn, 1=Churn): {prediction[0]}")
print(f"Probabilities [P(No churn), P(Churn)]: {proba[0]}")
print("\nSmoke test complete.")