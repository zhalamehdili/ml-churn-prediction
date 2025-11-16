# src/database.py
import os

from dotenv import load_dotenv
from sqlalchemy import Column, DateTime, Float, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func

# load variables from .env (at project root)
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set. Did you create .env?")

# engine & session factory
engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

# base model
Base = declarative_base()


class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    prediction_id = Column(String(50), unique=True, index=True)

    # customer fields
    gender = Column(String(10))
    senior_citizen = Column(Integer)
    partner = Column(String(10))
    dependents = Column(String(10))
    tenure = Column(Integer)
    phone_service = Column(String(10))
    multiple_lines = Column(String(30))
    internet_service = Column(String(30))
    online_security = Column(String(30))
    online_backup = Column(String(30))
    device_protection = Column(String(30))
    tech_support = Column(String(30))
    streaming_tv = Column(String(30))
    streaming_movies = Column(String(30))
    contract = Column(String(30))
    paperless_billing = Column(String(10))
    payment_method = Column(String(50))
    monthly_charges = Column(Float)
    total_charges = Column(Float)

    # prediction result
    churn_prediction = Column(String(10))
    churn_probability = Column(Float)
    risk_level = Column(String(10))

    # meta
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    model_version = Column(String(20), default="1.0")


class ModelMetrics(Base):
    __tablename__ = "model_metrics"

    id = Column(Integer, primary_key=True, index=True)
    model_version = Column(String(20))
    accuracy = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)

    trained_at = Column(DateTime(timezone=True), server_default=func.now())
    dataset_size = Column(Integer)
    notes = Column(Text, nullable=True)


def create_tables():
    """Create all DB tables."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Yield a DB session for FastAPI dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
