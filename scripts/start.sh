#!/bin/bash

set -e

echo "Starting Churn Prediction API..."

echo "Waiting for database and initializing tables..."
python src/init_db.py

echo "Database ready, starting API..."
uvicorn src.api:app --host 0.0.0.0 --port ${PORT:-8000}