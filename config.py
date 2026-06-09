import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Get API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Create client
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# Define model name
MODEL_NAME = "llama-3.1-8b-instant"