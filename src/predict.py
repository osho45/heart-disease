import joblib
import pandas as pd
import numpy as np
import os
import sys


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, '..', 'models')
MODEL_PATH = os.path.normpath(os.path.join(MODELS_DIR, 'best_model.joblib'))

def load_model(model_path):
    if not os.path.exists(model_path):
        print(f"Error: Model not found at {model_path}")
        sys.exit(1)
    return joblib.load(model_path)

def predict(model, data_dict):
    """
    Predicts heart disease risk for a single patient.
    Expects a dictionary with feature names matching the training data.
    """
   
    df = pd.DataFrame([data_dict])
    
    
    try:
        prediction = model.predict(df)[0]
        probability = model.predict_proba(df)[0][1] 
        return prediction, probability
    except Exception as e:
        print(f"Error during prediction: {e}")
        return None, None

if __name__ == "__main__":
    print(f"Loading model from {MODEL_PATH}...")
    model = load_model(MODEL_PATH)
    
    
    sample_patient = {
        'age': 63,
        'sex': 1,
        'cp': 3,
        'trestbps': 145,
        'chol': 233,
        'fbs': 1,
        'restecg': 0,
        'thalach': 150,
        'exang': 0,
        'oldpeak': 2.3,
        'slope': 0,
        'ca': 0,
        'thal': 1
    }
    
    print("-" * 30)
    print("Predicting for sample patient:")
    for k, v in sample_patient.items():
        print(f"  {k}: {v}")
    print("-" * 30)
    
    pred, prob = predict(model, sample_patient)
    
    if pred is not None:
        result = "Presence of heart disease" if pred == 1 else "No heart disease"
        print(f"\nResult: {result}")
        print(f"Probability: {prob:.4f}")
    
