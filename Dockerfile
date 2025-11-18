# base image with Python installed
FROM python:3.11-slim

# working directory inside the container
WORKDIR /app

# install the system tools needed for Python packages and database client
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# copy dependency file first to use Docker cache
COPY requirements.txt .

# install Python libraries listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# copy project files into the container
COPY . .

# make sure model and log folders exist inside the container
RUN mkdir -p models logs

# expose application port
EXPOSE 8000

# health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# run with dynamic PORT from Railway
CMD uvicorn src.api:app --host 0.0.0.0 --port ${PORT:-8000}