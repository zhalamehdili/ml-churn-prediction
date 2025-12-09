# Base image with Python installed
FROM python:3.11-slim

# Working directory inside the container
WORKDIR /app

# Install system tools needed for Python packages and PostgreSQL client
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file first to take advantage of Docker layer cache
COPY requirements.txt .

# Install Python libraries listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project into the container
COPY . .

# Make sure model and log folders exist inside the container
RUN mkdir -p models logs

# Expose application port (Railway will override this with $PORT)
EXPOSE 8000

# Container health check hitting the FastAPI /health endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run the FastAPI app with a dynamic port for Railway or 8000 by default
CMD uvicorn src.api:app --host 0.0.0.0 --port ${PORT:-8000}