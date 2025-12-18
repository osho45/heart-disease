import requests
import json

# Define the API endpoint
url = "http://localhost:8000/predict"

# Sample input data matching the Pydantic schema
payload = {
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

print(f"Sending request to {url}...")
print("Payload:", json.dumps(payload, indent=2))

try:
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        print("\nSuccess!")
        print("Response:", json.dumps(response.json(), indent=2))
    else:
        print(f"\nError {response.status_code}:")
        print(response.text)
except requests.exceptions.ConnectionError:
    print(f"\nCould not connect to {url}.")
    print("Is the API server running? (python api/main.py)")
