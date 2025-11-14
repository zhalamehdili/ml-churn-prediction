import sys
import time
import psycopg2
from psycopg2 import sql
import os

# make sure the project root (/app) is on the Python path when this script runs
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

def wait_for_db(max_retries=30, delay=2):
    """Wait for PostgreSQL to be ready inside Docker"""
    retries = 0
    while retries < max_retries:
        try:
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "db"),
                port=os.getenv("DB_PORT", "5432"),
                database=os.getenv("DB_NAME", "churn_db"),
                user=os.getenv("DB_USER", "churnuser"),
                password=os.getenv("DB_PASSWORD", "churnpass123"),
            )
            conn.close()
            print("database is reachable")
            return True
        except psycopg2.OperationalError:
            retries += 1
            print(f"waiting for database... ({retries}/{max_retries})")
            time.sleep(delay)

    print("database connection failed")
    return False


def init_database():
    """Initialize database tables and initial metrics inside Docker"""
    if not wait_for_db():
        sys.exit(1)

    # ensure /app is on sys.path so that 'import src...' works in the container
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if base_dir not in sys.path:
        sys.path.append(base_dir)

    from datetime import datetime
    from src.database import create_tables, SessionLocal, ModelMetrics

    print("creating database tables...")
    create_tables()

    db = SessionLocal()

    try:
        existing = db.query(ModelMetrics).filter_by(model_version="1.0").first()

        if not existing:
            initial_metrics = ModelMetrics(
                model_version="1.0",
                accuracy=0.852,
                precision=0.830,
                recall=0.810,
                f1_score=0.820,
                trained_at=datetime.utcnow(),
                dataset_size=7043,
                notes="Random Forest model for churn prediction in Docker setup",
            )
            db.add(initial_metrics)
            db.commit()
            print("initial model metrics inserted")
        else:
            print("model metrics already exist, skipping insert")

        print("database initialization complete")
    finally:
        db.close()


if __name__ == "__main__":
    init_database()