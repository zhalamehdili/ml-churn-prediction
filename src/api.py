import logging
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from .database import ModelMetrics, PredictionLog, get_db
from .predictor import ChurnPredictor
from .schemas import CustomerInput, HealthResponse, PredictionOutput

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Customer Churn Prediction API",
    description="Predict customer churn using machine learning with PostgreSQL logging",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

predictor = ChurnPredictor()


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Customer Churn Prediction API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "stats": "/stats",
            "history": "/history",
            "docs": "/docs",
        },
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check(db: Session = Depends(get_db)):
    # quick db ping
    try:
        db.execute(text("SELECT 1"))
        db_ok = True
    except Exception as e:
        logger.error(f"db health check failed: {e}")
        db_ok = False

    return HealthResponse(
        status="healthy" if db_ok else "degraded",
        model_loaded=predictor.loader.model is not None,
        timestamp=datetime.now(),
    )


@app.post("/predict", response_model=PredictionOutput, tags=["Prediction"])
def predict_churn(customer: CustomerInput, db: Session = Depends(get_db)):
    try:
        return predictor.predict(customer, db=db)
    except Exception as e:
        logger.exception("prediction failed")
        raise HTTPException(status_code=500, detail=f"prediction failed: {e}")


@app.get("/stats", tags=["Analytics"])
def get_statistics(db: Session = Depends(get_db)):
    total = db.query(PredictionLog).count()
    yes = db.query(PredictionLog).filter(PredictionLog.churn_prediction == "Yes").count()
    no = db.query(PredictionLog).filter(PredictionLog.churn_prediction == "No").count()

    probs = db.query(PredictionLog.churn_probability).all()
    avg_prob = (sum(p[0] for p in probs) / len(probs)) if probs else 0.0

    high = db.query(PredictionLog).filter(PredictionLog.risk_level == "High").count()
    med = db.query(PredictionLog).filter(PredictionLog.risk_level == "Medium").count()
    low = db.query(PredictionLog).filter(PredictionLog.risk_level == "Low").count()

    return {
        "total_predictions": total,
        "churn_predictions": {
            "yes": yes,
            "no": no,
            "churn_rate": round((yes / total) * 100, 2) if total else 0.0,
        },
        "average_churn_probability": round(avg_prob, 3),
        "risk_distribution": {"high": high, "medium": med, "low": low},
    }


@app.get("/history", tags=["Analytics"])
def get_history(limit: int = 10, db: Session = Depends(get_db)):
    rows = (
        db.query(PredictionLog)
        .order_by(PredictionLog.created_at.desc())
        .limit(limit)
        .all()
    )

    return {
        "total_returned": len(rows),
        "predictions": [
            {
                "prediction_id": r.prediction_id,
                "churn_prediction": r.churn_prediction,
                "churn_probability": r.churn_probability,
                "risk_level": r.risk_level,
                "tenure": r.tenure,
                "monthly_charges": r.monthly_charges,
                "contract": r.contract,
                "created_at": r.created_at.isoformat(),
            }
            for r in rows
        ],
    }


@app.get("/model-info", tags=["Info"])
def model_info(db: Session = Depends(get_db)):
    metrics = db.query(ModelMetrics).filter_by(model_version="1.0").first()
    return {
        "model_type": type(predictor.loader.model).__name__,
        "model_version": "1.0",
        "number_of_features": len(predictor.loader.feature_names),
        "features": predictor.loader.feature_names,
        "performance_metrics": (
            {
                "accuracy": metrics.accuracy,
                "precision": metrics.precision,
                "recall": metrics.recall,
                "f1_score": metrics.f1_score,
                "dataset_size": metrics.dataset_size,
            }
            if metrics
            else None
        ),
    }