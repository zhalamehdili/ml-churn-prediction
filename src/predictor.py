import pandas as pd
import numpy as np
from datetime import datetime
import uuid

from .model_loader import ModelLoader
from .schemas import CustomerInput, PredictionOutput

class ChurnPredictor:
    # wraps preprocessing + model inference
    def __init__(self):
        self.loader = ModelLoader()

    def _preprocess(self, customer: CustomerInput) -> np.ndarray:
        data = pd.DataFrame([customer.model_dump()])

        # encode categoricals using the exact encoders from training
        for col, enc in self.loader.label_encoders.items():
            if col in data.columns:
                try:
                    data[col] = enc.transform(data[col])
                except Exception:
                    # unseen category → fall back to most frequent class index 0
                    data[col] = 0

        # enforce training column order
        data = data[self.loader.feature_names]

        # scale numeric features
        return self.loader.scaler.transform(data)

    def predict(self, customer: CustomerInput) -> PredictionOutput:
        X = self._preprocess(customer)
        pred = int(self.loader.model.predict(X)[0])
        proba = self.loader.model.predict_proba(X)[0][1]  # class=1

        risk = "Low" if proba < 0.3 else ("Medium" if proba < 0.7 else "High")

        return PredictionOutput(
            customer_id=f"pred_{uuid.uuid4().hex[:8]}",
            churn_prediction="Yes" if pred == 1 else "No",
            churn_probability=round(float(proba), 3),
            risk_level=risk,
            timestamp=datetime.now(),
        )