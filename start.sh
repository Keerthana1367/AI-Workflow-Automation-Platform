#!/bin/bash

# Start the FastAPI Backend in the background
echo "Starting FastAPI Backend..."
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Wait for backend to wake up
sleep 5

# Start the Streamlit Frontend
echo "Starting Streamlit Frontend..."
# Using 127.0.0.1 for maximum compatibility inside the container
export API_URL="http://127.0.0.1:8000/api"
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
