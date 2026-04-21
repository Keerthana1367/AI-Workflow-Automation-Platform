@echo off
echo ==========================================
echo Starting AI Workflow Platform...
echo ==========================================

:: Check if GEMINI_API_KEY is set
if not exist .env (
    echo [WARNING] .env file not found. Please create one with GEMINI_API_KEY.
)

:: Start Backend
echo [1/2] Starting FastAPI Backend on port 8000...
start /B uvicorn main:app --host 0.0.0.0 --port 8000

:: Wait for backend
echo Waiting for backend to initialize...
timeout /t 5 /nobreak > nul

:: Start Frontend
echo [2/2] Starting Streamlit Frontend...
set API_URL=http://localhost:8000/api
streamlit run app.py

pause
