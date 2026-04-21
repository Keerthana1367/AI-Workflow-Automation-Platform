#!/bin/bash

# Start the FastAPI Backend in the background
echo "Starting FastAPI Backend..."
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Wait for backend to wake up
sleep 5

# Set Streamlit configurations via Env Vars
# We force it to be a number to avoid the "$PORT" literal string error
REAL_PORT=$(echo $PORT | tr -cd '0-9')
export STREAMLIT_SERVER_PORT=${REAL_PORT:-8501}
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export API_URL="http://127.0.0.1:8000/api"

echo "Starting Streamlit Frontend on port $STREAMLIT_SERVER_PORT..."
streamlit run app.py
