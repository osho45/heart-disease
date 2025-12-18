# Heart Disease Classification: End-to-End Pipeline

This repository contains a full-stack Machine Learning project for predicting heart disease. It implements a complete pipeline from raw data to a deployed application, featuring database normalization, experiment tracking, and containerized deployment.

## � Project Structure

```
├── api/                   # FastAPI Backend
│   ├── main.py
│   └── Dockerfile
├── ui/                    # Streamlit Frontend
│   ├── app.py
│   ├── streamlit_options.json
│   └── Dockerfile
├── notebooks/             # Jupyter Notebooks
│   └── heart_classification.ipynb  # Training pipeline & experiments
├── src/                   # Source Code
│   ├── db_utils.py        # Database normalization & loading
│   └── predict.py         # CLI Inference script
├── models/                # Trained Models
│   ├── best_model.joblib
│   └── best_model_metadata.json
├── Data/                  # Dataset & Database
│   ├── heart.csv
│   └── heart.db
├── docker-compose.yml     # Container Orchestration
└── requirements.txt       # Dependencies
```

## ✅ Grading Checklist

| Deliverable | Implementation Details | Location |
| :--- | :--- | :--- |
| **Dataset** | Binary classification using `heart.csv`. | `Data/heart.csv` |
| **Database** | Normalized SQLite schema (3NF) with `patients`, `exams`, and lookup tables. | `src/db_utils.py`, `notebooks/` |
| **Experimentation** | 16 controlled runs: 4 Algorithms (LogReg, RF, SVC, GBM) × 4 Setup Conditions. | `notebooks/heart_classification.ipynb` |
| **Tracking** | MLflow tracking for parameters, metrics (F1 score), and artifacts. | MLflow / DagsHub |
| **Best Model** | Automated selection and validaton of the highest performing model. | `models/best_model.joblib` |
| **API Deployment** | RESTful API built with FastAPI and Pydantic validation. | `api/main.py` |
| **UI Dashboard** | Interactive Streamlit app with history logging to SQLite. | `ui/app.py` |
| **Docker** | Full application containerization using Docker Compose. | `docker-compose.yml` |

## 🚀 How to Run

### Using Docker (Recommended)
The easiest way to run the full application.

1.  **Start Services**:
    ```bash
    docker-compose up --build
    ```
2.  **Access Application**:
    *   **Frontend (Streamlit)**: [http://localhost:8501](http://localhost:8501)
    *   **Backend Docs (FastAPI)**: [http://localhost:8000/docs](http://localhost:8000/docs)

### Running Locally (Manual)
If you prefer not to use Docker:

1.  **Install Dependencies**:
    ```bash
    python -m pip install -r requirements.txt
    python -m pip install -r ui/requirements.txt
    ```
2.  **Run API** (Background or separate terminal):
    ```bash
    python api/main.py
    ```
3.  **Run Frontend**:
    ```bash
    streamlit run ui/app.py
    ```

## ☁️ Deployment Guide (DigitalOcean)

To deploy to a cloud VPS (e.g., DigitalOcean Droplet):

1.  **Provision**: Create a Droplet (Ubuntu or Docker image).
2.  **Clone**: SSH into the server and clone this repository.
3.  **Configure**: Set environment variables (e.g., `MLFLOW_TRACKING_URI`) if needed.
4.  **Launch**:
    ```bash
    docker-compose up -d --build
    ```
5.  **Access**: Open your browser to `http://<your-droplet-ip>:8501`.

## 🔬 Development

*   **Training**: Run `jupyter notebook notebooks/heart_classification.ipynb` to re-run experiments.
*   **Inference**: Run `python src/predict.py` for a quick command-line prediction test.
