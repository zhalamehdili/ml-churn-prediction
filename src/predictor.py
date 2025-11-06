import pandas as pd
import numpy as np
from datetime import datetime
import uuid
import logging
from sqlalchemy.orm import Session

from .model_loader import ModelLoader
from .schemas import CustomerInput, PredictionOutput
from .database import PredictionLog

logger = logging.getLogger(__name__)

class ChurnPredictor:
    """Handles churn prediction logic"""

    def __init__(self):
        self.loader = ModelLoader()

    def _preprocess_input(self, customer_data: CustomerInput) -> np.ndarray:
        """Convert input data to model-ready format"""

        # Convert to dictionary -> DataFrame
        data_dict = customer_data.model_dump()
        df = pd.DataFrame([data_dict])

        # Encode categorical variables using saved encoders
        for col, encoder in self.loader.label_encoders.items():
            if col in df.columns:
                try:
                    df[col] = encoder.transform(df[col])
                except ValueError:
                    # unseen category -> fallback to 0 (or most common)
                    df[col] = 0

        # Ensure correct column order
        df = df.reindex(columns=self.loader.feature_names, fill_value=0)

        # Scale features
        scaled_data = self.loader.scaler.transform(df)
        return scaled_data

    def predict(self, customer_data: CustomerInput, db: Session = None) -> PredictionOutput:
        """Make churn prediction and (optionally) log into database"""

        # Preprocess
        X = self._preprocess_input(customer_data)

        # Predict
        pred_class = self.loader.model.predict(X)[0]
        proba = self.loader.model.predict_proba(X)[0]
        churn_prob = float(proba[1])

        churn_prediction = "Yes" if pred_class == 1 else "No"
        if churn_prob < 0.3:
            risk_level = "Low"
        elif churn_prob < 0.7:
            risk_level = "Medium"
        else:
            risk_level = "High"

        prediction_id = f"pred_{uuid.uuid4().hex[:8]}"

        # Log to DB if session provided
        if db is not None:
            try:
                log_entry = PredictionLog(
                    prediction_id=prediction_id,
                    gender=customer_data.gender,
                    senior_citizen=customer_data.SeniorCitizen,
                    partner=customer_data.Partner,
                    dependents=customer_data.Dependents,
                    tenure=customer_data.tenure,
                    phone_service=customer_data.PhoneService,
                    multiple_lines=customer_data.MultipleLines,
                    internet_service=customer_data.InternetService,
                    online_security=customer_data.OnlineSecurity,
                    online_backup=customer_data.OnlineBackup,
                    device_protection=customer_data.DeviceProtection,
                    tech_support=customer_data.TechSupport,
                    streaming_tv=customer_data.StreamingTV,
                    streaming_movies=customer_data.StreamingMovies,
                    contract=customer_data.Contract,
                    paperless_billing=customer_data.PaperlessBilling,
                    payment_method=customer_data.PaymentMethod,
                    monthly_charges=customer_data.MonthlyCharges,
                    total_charges=customer_data.TotalCharges,
                    churn_prediction=churn_prediction,
                    churn_probability=churn_prob,
                    risk_level=risk_level,
                    model_version="1.0",
                )
                db.add(log_entry)
                db.commit()
                logger.info(f"prediction {prediction_id} logged to DB")
            except Exception as e:
                logger.error(f"DB log failed: {e}")
                db.rollback()

        return PredictionOutput(
            customer_id=prediction_id,
            churn_prediction=churn_prediction,
            churn_probability=round(churn_prob, 3),
            risk_level=risk_level,
            timestamp=datetime.now(),
        )