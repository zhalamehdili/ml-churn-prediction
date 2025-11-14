# Customer Churn Prediction (ML Pipeline + FastAPI + PostgreSQL + Docker)

This project predicts customer churn using a complete machine learning pipeline and a backend built with FastAPI.
It is based on the Telco Customer Churn dataset and extends a training notebook into a fully working backend API with a connected PostgreSQL database and Dockerized deployment.

## 1. Overview

The goal is to identify customers who are likely to stop using the service (churn) by analyzing demographic, usage, and contract data.
The project started as a Jupyter model training task and evolved into an end-to-end system including API engineering, database integration, analytics and Docker deployment.

## 2. What was implemented

- Explored and cleaned the Telco dataset (EDA)
- Trained and compared Logistic Regression and Random Forest models
- Evaluated models using accuracy, precision, recall and F1
- Saved the trained model and preprocessing pipeline
- Built a FastAPI application to serve predictions in real time
- Integrated PostgreSQL for storing predictions and metadata
- Added endpoints for health checks, statistics and prediction history
- Implemented automated API tests using pytest
- Containerized the entire application using Docker and docker-compose
- Created helper scripts for Docker start, stop, rebuild, and logs

## 3. Results

| Model | Accuracy | F1 |
| ------ | -------- | ------ |
| Logistic Regression | 0.799 | 0.592 |
| Random Forest | 0.852 | 0.820 |

The Random Forest model is used in the API.
All predictions (with probability and risk level) are stored in PostgreSQL.

## 4. Tech Stack

- Python (pandas, numpy, scikit-learn)
- FastAPI + Uvicorn
- PostgreSQL with SQLAlchemy ORM
- Pydantic for request/response models
- pytest for testing
- Docker & docker-compose for deployment

## 5. Project Structure

ml-churn-prediction/
├── data/             # Dataset (churn.csv)
├── models/           # Saved ML models and preprocessing files
├── notebooks/        # Training and EDA notebooks
├── src/              # FastAPI code (API, DB, predictor, loader)
├── scripts/          # Docker helper scripts
├── tests/            # API tests
├── Dockerfile
├── docker-compose.yml
└── requirements.txt

## 6. API Endpoints

- POST /predict — Run a churn prediction and save result in DB
- GET /health — Check API and DB status
- GET /stats — Get churn rate and prediction analytics
- GET /history — List recent predictions
- GET /model-info — View model version and stored metrics

Swagger UI:
http://localhost:8000/docs

## 7. Docker Usage 

Start all services:
docker-compose up

Run in background:
docker-compose up -d

Stop containers:
docker-compose down

Rebuild after code changes:
docker-compose up --build

Follow API logs:
docker-compose logs -f api

Access PostgreSQL:
docker exec -it churn-postgres psql -U churnuser -d churn_db

All predictions persist across restarts using Docker volumes.