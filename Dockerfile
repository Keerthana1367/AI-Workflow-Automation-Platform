FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies (for OCR and Healthcheck)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Ensure DB is ignored in local builds but this is for production
# platform.db is in .gitignore so it won't be copied if .git is there

# Fix line endings and permissions
RUN sed -i 's/\r$//' start.sh && chmod +x start.sh

# Railway uses $PORT. We handle this inside start.sh
# CMD uses shell form to ensure $PORT is available
CMD ["/bin/bash", "-c", "./start.sh"]
