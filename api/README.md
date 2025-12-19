# Heart Disease Prediction API

FastAPI backend to serve the best trained heart classification model.

## Setup

```bash
python -m pip install -r requirements.txt
```

## Running the API

Run from the `api/` directory:

```bash
cd api
python main.py
```
Or with uvicorn directly:
```bash
uvicorn main:app --reload
```

## Testing (Local)

Check health:
```bash
curl http://localhost:8000/health
```

Predict (Sample):
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"age": 63, "sex": 1, "cp": 3, "trestbps": 145, "chol": 233, "fbs": 1, "restecg": 0, "thalach": 150, "exang": 0, "oldpeak": 2.3, "slope": 0, "ca": 0, "thal": 1}'
```
