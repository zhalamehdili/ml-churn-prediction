# Railway Deployment Guide

This document explains how I deploy the Customer Churn Prediction API to Railway using Docker and PostgreSQL, starting from this GitHub repository.

Live instance (current project):  
API base URL: https://ml-churn-prediction-production-1ab7.up.railway.app  
Docs: https://ml-churn-prediction-production-1ab7.up.railway.app/docs  

---

## 1. Architecture

- Platform: Railway  
- Compute: Docker container built from this repository  
- Backend: FastAPI + Uvicorn  
- Database: Railway PostgreSQL  
- ORM: SQLAlchemy  
- Model: Random Forest classifier loaded from files in models/  
- Storage: Prediction logs and model metrics in PostgreSQL  
- CI/CD: GitHub → Railway auto-deploy from main branch  

Railway provides the domain, SSL and infrastructure. I push code to GitHub, Railway builds the Docker image and redeploys the container automatically.

---

## 2. Initial Railway Setup

### 2.1 Create account and project

1. Go to https://railway.app  
2. Sign in with GitHub  
3. Click New Project  
4. Choose Deploy from GitHub repo  
5. Select this repository: ml-churn-prediction  
6. Railway detects the Dockerfile and starts the first build  

After the first build finishes, Railway creates a service for the API.

### 2.2 Add PostgreSQL

1. In the same project click New  
2. Select Database  
3. Choose PostgreSQL  
4. Wait until the database is provisioned  

Railway links the database to the API service and creates a DATABASE_URL environment variable that FastAPI uses.

---

## 3. Configuration Files

### 3.1 Dockerfile

The container must listen on the port Railway sets in PORT:

EXPOSE 8000  
CMD uvicorn src.api:app --host 0.0.0.0 --port ${PORT:-8000}

The fallback allows the app to run locally without PORT defined.

### 3.2 railway.json

This tells Railway to build everything using the Dockerfile:

{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}

This file lives in the project root.

---

## 4. Environment Variables

Railway automatically sets:

- PORT  
- DATABASE_URL  

For local development I use .env:

DATABASE_URL=postgresql://churnuser:churnpassword@localhost:5432/churn_db  
API_HOST=0.0.0.0  
API_PORT=8000  

On Railway I only need DATABASE_URL. PORT is injected automatically.

---

## 5. Database Initialization

The API exposes an admin endpoint that creates tables and inserts model metrics.

Once the deployment is healthy, I run:

curl -X POST https://ml-churn-prediction-production-1ab7.up.railway.app/admin/init-db

This:

- Creates all tables if they do not exist  
- Inserts initial model metrics for version 1.0 if missing  

This must be done once per environment.

---

## 6. Checking the Live API

Health check:

curl https://ml-churn-prediction-production-1ab7.up.railway.app/health

Example prediction:

curl -X POST https://ml-churn-prediction-production-1ab7.up.railway.app/predict -H "Content-Type: application/json" -d '{"gender":"Female","SeniorCitizen":0,"Partner":"Yes","Dependents":"No","tenure":24,"PhoneService":"Yes","MultipleLines":"No","InternetService":"Fiber optic","OnlineSecurity":"No","OnlineBackup":"Yes","DeviceProtection":"No","TechSupport":"No","StreamingTV":"Yes","StreamingMovies":"No","Contract":"Month-to-month","PaperlessBilling":"Yes","PaymentMethod":"Electronic check","MonthlyCharges":70.5,"TotalCharges":1692.0}'

Statistics:

curl https://ml-churn-prediction-production-1ab7.up.railway.app/stats

History:

curl https://ml-churn-prediction-production-1ab7.up.railway.app/history

Swagger UI:  
https://ml-churn-prediction-production-1ab7.up.railway.app/docs  

---

## 7. Redeploying

Every time I push to main, Railway redeploys automatically:

git add .  
git commit -m "Update deployment"  
git push origin main  

Railway:

1. Pulls the commit  
2. Builds Docker image  
3. Starts new container  
4. Switches traffic when the app is healthy  

Build logs appear under Deployments in Railway.

---

## 8. Railway CLI (optional)

Install CLI:

npm install -g @railway/cli

Log in:

railway login

Link project:

railway link

View logs:

railway logs

Open dashboard:

railway open

---

## 9. Troubleshooting

Common issues:

- Missing DATABASE_URL  
- Wrong port usage  
- Missing Python dependencies  
- Dockerfile command incorrect  

If / and /health work but /predict fails:
Likely a database or model loading issue.

If nothing works:
Check container logs in Railway.

---

## 10. Summary

- Code stored in GitHub  
- Railway builds via railway.json  
- Database is auto-linked  
- App listens on PORT and exposes /predict, /stats, /history, /health, /model-info  
- Deployments happen on git push  

This completes the full deployment workflow.