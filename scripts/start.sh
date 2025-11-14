#!/bin/bash

echo "starting churn prediction API container"

echo "waiting for database to be ready"
python scripts/init_db_docker.py

if [ $? -eq 0 ]; then
    echo "database is ready, starting API server"
    python -m uvicorn src.api:app --host 0.0.0.0 --port 8000
else
    echo "database initialization failed, container will exit"
    exit 1
fi