# Railway Deployment Guide

This document explains how I deploy the **Customer Churn Prediction API** to Railway using Docker and PostgreSQL, starting from this GitHub repository.

Live instance (current project):  
**API base URL:** https://ml-churn-prediction-production-lab7.up.railway.app  
**Docs:** https://ml-churn-prediction-production-lab7.up.railway.app/docs  

---

## 1. Architecture

- **Platform:** Railway
- **Compute:** Docker container built from this repo
- **Backend:** FastAPI + Uvicorn
- **Database:** Railway PostgreSQL
- **ORM:** SQLAlchemy
- **Model:** Random Forest classifier loaded from `models/`
- **Storage:** Prediction logs and model metrics in PostgreSQL
- **CI/CD:** GitHub → Railway auto-deploy from `main` branch

Railway provides the domain, SSL and infrastructure. I only push code to GitHub, Railway builds and redeploys the container automatically.

---

## 2. Initial Railway Setup

### 2.1 Create account and project

1. Go to https://railway.app
2. Sign in with GitHub
3. Click **New Project**
4. Choose **Deploy from GitHub repo**
5. Select this repository: `ml-churn-prediction`
6. Railway detects the `Dockerfile` and starts the first build

After the build finishes, Railway creates a service for the API.

### 2.2 Add PostgreSQL

1. In the same project click **New**
2. Select **Database**
3. Choose **PostgreSQL**
4. Wait until the database service is provisioned

Railway automatically exposes the database to the API service and creates a `DATABASE_URL` variable.

---

## 3. Configuration Files

### 3.1 Dockerfile

The Dockerfile builds the image and runs Uvicorn with the port provided by Railway:

```dockerfile
# Expose default port (Railway overrides this with $PORT)
EXPOSE 8000

# Run the FastAPI app with Railway's dynamic port
CMD uvicorn src.api:app --host 0.0.0.0 --port ${PORT:-8000}