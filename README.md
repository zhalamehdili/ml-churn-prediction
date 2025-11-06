# Customer Churn Prediction (ML Pipeline + FastAPI + PostgreSQL)

This project predicts customer churn using a complete machine learning pipeline and backend integration in Python.  
It’s based on the Telco Customer Churn dataset and extends my earlier training notebook into a working backend API with a connected database for prediction logging.

## 1. Overview

The goal is to identify customers who are likely to stop using the service (churn) by analyzing demographic, usage, and contract data.  
The project started as a model training task and evolved into an end-to-end backend system using FastAPI and PostgreSQL.

## 2. What I Did

- Cleaned and explored the Telco dataset (EDA)
- Trained and compared Logistic Regression and Random Forest models
- Evaluated models using accuracy and F1 score
- Saved trained models and preprocessing objects for later use
- Built a FastAPI application to serve predictions in real time
- Connected a PostgreSQL database to store each prediction and its probability
- Added API endpoints for health checks, statistics, and prediction history
- Wrote automated tests using pytest to verify endpoints and data flow

## 3. Results

| Model | Accuracy | F1 |
|--------|-----------|------|
| Logistic Regression | 0.799 | 0.592 |
| Random Forest | 0.852 | 0.820 |

(Accuracy and F1 are based on the training phase. API results include live predictions logged in the database.)

## 4. Tech Stack

- Python 3.13  
- pandas, numpy, scikit-learn  
- FastAPI for the backend  
- PostgreSQL for database integration  
- SQLAlchemy and Pydantic for data management  
- pytest for testing  
- Docker planned for containerization  

## 5. Project Structure

ml-churn-prediction/
├── data/             # Dataset (churn.csv)
├── models/           # Saved models and preprocessing files
├── notebooks/        # Training and analysis notebooks
├── src/              # FastAPI source code (API, DB, predictor)
├── tests/            # Automated API tests
└── requirements.txt

## 6. API Endpoints

- **POST /predict** – Make a churn prediction and log it to the database  
- **GET /health** – Check model and database status  
- **GET /stats** – View churn prediction statistics and risk distribution  
- **GET /history** – Retrieve recent prediction history  
- **GET /model-info** – View model metadata and metrics  

All endpoints are documented and testable via Swagger UI at  
`http://localhost:8000/docs`

## 7. Next Steps

- Containerize the application with Docker  
- Automate deployment using CI/CD  
- Deploy on Azure or another cloud environment  
- Add visualization or monitoring for churn trends  

---

This project helped me understand how to connect machine learning, backend development, and databases in one system.  
It’s currently running locally with a working API and database integration and will be prepared for containerization and deployment next.