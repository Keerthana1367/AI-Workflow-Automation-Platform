#!/bin/bash

# Start the FastAPI backend
echo "Starting FastAPI Backend..."
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
