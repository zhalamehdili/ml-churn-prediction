# src/init_db.py
from datetime import datetime

from src.database import ModelMetrics, SessionLocal, create_tables


def init_database():
    print("Creating database tables...")
    create_tables()

    db = SessionLocal()
    try:
        existing = db.query(ModelMetrics).filter_by(model_version="1.0").first()
        if not existing:
            metrics = ModelMetrics(
                model_version="1.0",
                accuracy=0.852,  # replace with YOUR real numbers if different
                precision=0.830,
                recall=0.810,
                f1_score=0.820,
                trained_at=datetime.utcnow(),
                dataset_size=7043,
                notes="Random Forest model trained on Telco dataset",
            )
            db.add(metrics)
            db.commit()
            print("✔ Initial model metrics added")
        else:
            print("ℹ Model metrics already exist")
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
