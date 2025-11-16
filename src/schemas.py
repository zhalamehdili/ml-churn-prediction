from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class CustomerInput(BaseModel):
    # request body I’ll send to /predict
    gender: Literal["Male", "Female"] = Field(..., description="Customer gender")
    SeniorCitizen: Literal[0, 1] = Field(..., description="0=No, 1=Yes")
    Partner: Literal["Yes", "No"] = Field(..., description="Has partner")
    Dependents: Literal["Yes", "No"] = Field(..., description="Has dependents")
    tenure: int = Field(..., ge=0, le=100, description="Months with company")
    PhoneService: Literal["Yes", "No"] = Field(..., description="Phone service")
    MultipleLines: Literal["Yes", "No", "No phone service"] = Field(..., description="Multiple lines")
    InternetService: Literal["DSL", "Fiber optic", "No"] = Field(..., description="Internet type")
    OnlineSecurity: Literal["Yes", "No", "No internet service"] = Field(..., description="Online security")
    OnlineBackup: Literal["Yes", "No", "No internet service"] = Field(..., description="Online backup")
    DeviceProtection: Literal["Yes", "No", "No internet service"] = Field(..., description="Device protection")
    TechSupport: Literal["Yes", "No", "No internet service"] = Field(..., description="Tech support")
    StreamingTV: Literal["Yes", "No", "No internet service"] = Field(..., description="Streaming TV")
    StreamingMovies: Literal["Yes", "No", "No internet service"] = Field(..., description="Streaming movies")
    Contract: Literal["Month-to-month", "One year", "Two year"] = Field(..., description="Contract type")
    PaperlessBilling: Literal["Yes", "No"] = Field(..., description="Paperless billing")
    PaymentMethod: Literal[
        "Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"
    ] = Field(..., description="Payment method")
    MonthlyCharges: float = Field(..., ge=0, description="Monthly charges")
    TotalCharges: float = Field(..., ge=0, description="Total charges")


class PredictionOutput(BaseModel):
    # response body I’ll return from /predict
    customer_id: str = Field(..., description="Unique identifier")
    churn_prediction: Literal["Yes", "No"] = Field(..., description="Churn?")
    churn_probability: float = Field(..., ge=0, le=1, description="Probability 0-1")
    risk_level: Literal["Low", "Medium", "High"] = Field(..., description="Risk bucket")
    timestamp: datetime = Field(..., description="Prediction time")


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    timestamp: datetime
