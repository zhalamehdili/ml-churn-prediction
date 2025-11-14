#!/bin/bash
echo "starting Docker containers for the churn prediction project"
docker-compose up -d
echo "containers are running"
echo "API docs available at http://localhost:8000/docs"