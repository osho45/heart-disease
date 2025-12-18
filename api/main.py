from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os
import uvicorn

# Define paths
# resolving relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, '..', 'models')
MODEL_PATH = os.path.normpath(os.path.join(MODELS_DIR, 'best_model.joblib'))

app = FastAPI(
    title="Heart Disease Prediction API",
    description="API to predict heart disease risk using a trained ML model.",
    version="1.0.0"
)

# Load Model at startup
model = None

@app.on_event("startup")
def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print(f"Model loaded from {MODEL_PATH}")
    else:
        print(f"Warning: Model not found at {MODEL_PATH}")

# Input Schema
class HeartDiseaseInput(BaseModel):
    age: int
    sex: int
    cp: int
    trestbps: int
    chol: int
    fbs: int
    restecg: int
    thalach: int
    exang: int
    oldpeak: float
    slope: int
    ca: int
    thal: int

    class Config:
        schema_extra = {
            "example": {
                "age": 63,
                "sex": 1,
                "cp": 3,
                "trestbps": 145,
                "chol": 233,
                "fbs": 1,
                "restecg": 0,
                "thalach": 150,
                "exang": 0,
                "oldpeak": 2.3,
                "slope": 0,
                "ca": 0,
                "thal": 1
            }
        }

@app.get("/health")
def health_check():
    return {"status": "ok", "model_loaded": model is not None}

@app.post("/predict")
def predict(input_data: HeartDiseaseInput):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Convert Pydantic model to dict, then to DataFrame
        data_dict = input_data.dict()
        df = pd.DataFrame([data_dict])
        
        # Predict
        prediction = model.predict(df)[0]
        # Get probability of class 1
        probability = model.predict_proba(df)[0][1]
        
        result_str = "Presence of heart disease" if prediction == 1 else "No heart disease"
        
        return {
            "prediction": int(prediction),
            "probability": float(probability),
            "result": result_str
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
