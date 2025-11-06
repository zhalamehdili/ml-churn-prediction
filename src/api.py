from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging

from .schemas import CustomerInput, PredictionOutput, HealthResponse
from .predictor import ChurnPredictor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Customer Churn Prediction API",
    description="Predict customer churn using my trained model",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # narrow this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

predictor = ChurnPredictor()

@app.get("/", tags=["root"])
def root():
    return {
        "message": "Customer Churn Prediction API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {"health": "/health", "predict": "/predict", "docs": "/docs"},
    }

@app.get("/health", response_model=HealthResponse, tags=["health"])
def health():
    return HealthResponse(
        status="healthy",
        model_loaded=predictor.loader.model is not None,
        timestamp=datetime.now(),
    )

@app.post("/predict", response_model=PredictionOutput, tags=["prediction"])
def predict(customer: CustomerInput):
    try:
        return predictor.predict(customer)
    except Exception as e:
        logger.exception("prediction failed")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

@app.get("/model-info", tags=["info"])
def model_info():
    return {
        "model_type": type(predictor.loader.model).__name__,
        "number_of_features": len(predictor.loader.feature_names),
        "features": predictor.loader.feature_names,
        "encoders": list(predictor.loader.label_encoders.keys()),
    }