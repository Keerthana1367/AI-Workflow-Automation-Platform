#!/bin/bash

# Start the FastAPI Backend in the background
echo "Starting FastAPI Backend..."
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Wait for backend to wake up
sleep 5

# Use Railway's PORT or default to 8501
export PORT="${PORT:-8501}"

# Start the Streamlit Frontend
echo "Starting Streamlit Frontend on port $PORT..."
# Using 127.0.0.1 for internal backend communication
export API_URL="http://127.0.0.1:8000/api"
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
