#!/bin/bash

echo "Starting Churn Prediction API..."

# wait for database
echo "Waiting for database..."
python scripts/init_db_docker.py

if [ $? -eq 0 ]; then
    echo "Database ready, starting API..."
    # use Railway's PORT or default to 8000
    uvicorn src.api:app --host 0.0.0.0 --port ${PORT:-8000}
else
    echo "Database initialization failed!"
    exit 1
fi