# tests/test_api.py
from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "running"

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "healthy"
    assert isinstance(data["model_loaded"], bool)

def test_predict_ok():
    payload = {
        "gender": "Male",
        "SeniorCitizen": 0,
        "Partner": "Yes",
        "Dependents": "No",
        "tenure": 24,
        "PhoneService": "Yes",
        "MultipleLines": "No",
        "InternetService": "Fiber optic",
        "OnlineSecurity": "No",
        "OnlineBackup": "Yes",
        "DeviceProtection": "No",
        "TechSupport": "No",
        "StreamingTV": "Yes",
        "StreamingMovies": "No",
        "Contract": "Month-to-month",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Electronic check",
        "MonthlyCharges": 70.5,
        "TotalCharges": 1692.0
    }
    r = client.post("/predict", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["churn_prediction"] in ["Yes", "No"]
    assert 0 <= data["churn_probability"] <= 1
    assert data["risk_level"] in ["Low", "Medium", "High"]
    assert "customer_id" in data

def test_model_info():
    r = client.get("/model-info")
    assert r.status_code == 200
    data = r.json()
    assert "model_type" in data
    assert "number_of_features" in data
    assert isinstance(data["features"], list)

def test_validation_error():
    # tenure must be int; send string to force 422
    bad = {"gender": "Male", "tenure": "oops"}
    r = client.post("/predict", json=bad)
    assert r.status_code == 422