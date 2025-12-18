import streamlit as st
import requests
import json
import sqlite3
import pandas as pd
import os
import datetime

# --- Configuration ---
# --- Configuration ---
API_URL = os.getenv("API_URL", "http://localhost:8000/predict")
# Use a data directory for persistence
DB_FOLDER = "data"
if not os.path.exists(DB_FOLDER):
    os.makedirs(DB_FOLDER)
DB_NAME = os.path.join(DB_FOLDER, "predictions.db")

# --- SQLite Setup ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            input_data TEXT,
            prediction INTEGER,
            probability REAL,
            result TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_prediction(input_data, prediction, probability, result):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO predictions (timestamp, input_data, prediction, probability, result)
        VALUES (?, ?, ?, ?, ?)
    ''', (datetime.datetime.now(), json.dumps(input_data), prediction, probability, result))
    conn.commit()
    conn.close()

def get_recent_predictions(limit=5):
    conn = sqlite3.connect(DB_NAME)
    # Read into DataFrame for easy display
    try:
        df = pd.read_sql_query(f"SELECT timestamp, probability, result, input_data FROM predictions ORDER BY id DESC LIMIT {limit}", conn)
    except:
        df = pd.DataFrame()
    conn.close()
    return df

# Initialize DB on app load
init_db()

# --- UI Setup ---
st.set_page_config(page_title="Heart Disease Predictor", layout="wide")
st.title("Heart Disease Prediction Dashboard")

# Load Options
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OPTIONS_PATH = os.path.join(BASE_DIR, "streamlit_options.json")

with open(OPTIONS_PATH, "r") as f:
    options = json.load(f)

user_input = {}

st.subheader("Patient Features")

# Create a form-like layout with columns
# We have 13 features. Let's do 4 columns.
input_cols = st.columns(4)
col_idx = 0

# 1. Numerical Features (using Number Input for precise editing)
for field, range_val in options["slider_fields"].items():
    min_v, max_v = range_val
    # Determine step and type
    is_float = isinstance(min_v, float) or isinstance(max_v, float)
    step = 0.1 if is_float else 1
    default_v = (min_v + max_v) / 2
    if not is_float:
        default_v = int(default_v)
        
    with input_cols[col_idx % 4]:
        user_input[field] = st.number_input(
            f"{field.capitalize()}",
            min_value=min_v,
            max_value=max_v,
            value=default_v,
            step=step
        )
    col_idx += 1

# 2. Categorical Features
for field, values in options["single_select_fields"].items():
    with input_cols[col_idx % 4]:
        user_input[field] = st.selectbox(f"{field.capitalize()}", values)
    col_idx += 1

st.divider()

# --- Prediction Section ---
result_col, history_col = st.columns([1, 1])

with result_col:
    st.subheader("Prediction")
    # Preview Input
    with st.expander("View Input Payload", expanded=False):
        st.json(user_input)

    if st.button("Predict Risk", type="primary", use_container_width=True):
        with st.spinner("Consulting the model..."):
            try:
                # Call API
                response = requests.post(API_URL, json=user_input)
                
                if response.status_code == 200:
                    result_data = response.json()
                    
                    pred_class = result_data["prediction"]
                    prob = result_data["probability"]
                    result_text = result_data["result"]
                    
                    # Display Result
                    if pred_class == 1:
                        st.error(f"**Prediction:** {result_text}")
                    else:
                        st.success(f"**Prediction:** {result_text}")
                    
                    st.metric("Probability of Disease", f"{prob:.2%}")
                    
                    # Log to DB
                    log_prediction(user_input, pred_class, prob, result_text)
                    st.toast("Prediction logged successfully!")
                    
                else:
                    st.error(f"API Error: {response.status_code} - {response.text}")
            except requests.exceptions.ConnectionError:
                st.error(f"Could not connect to API at {API_URL}. Is it running?")

with history_col:
    st.subheader("Recent Predictions")
    recent_df = get_recent_predictions()
    if not recent_df.empty:
        st.dataframe(recent_df[["timestamp", "result", "probability"]], hide_index=True)
    else:
        st.info("No predictions yet.")

