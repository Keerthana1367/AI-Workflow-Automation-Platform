#!/bin/bash

# Start the FastAPI Backend in the background
echo "Starting FastAPI Backend..."
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Wait for backend to wake up
sleep 5

# Set Streamlit configurations via Env Vars (more robust than CLI flags in some shells)
# This avoids the "$PORT is not a valid integer" error
export STREAMLIT_SERVER_PORT=${PORT:-8501}
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export API_URL="http://127.0.0.1:8000/api"

echo "Starting Streamlit Frontend on port $STREAMLIT_SERVER_PORT..."
streamlit run app.py
