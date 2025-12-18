# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY ui/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY ui /app/ui

# Expose port
EXPOSE 8501

# Environment variable for API URL (can be overridden by compose)
ENV API_URL=http://localhost:8000/predict

# Run command
# We run from /app, targeting ui/app.py
CMD ["streamlit", "run", "ui/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
