#!/bin/bash
echo "rebuilding Docker containers for the churn prediction project"
docker-compose down
docker-compose build --no-cache
docker-compose up -d
echo "rebuild complete"
echo "API docs available at http://localhost:8000/docs"