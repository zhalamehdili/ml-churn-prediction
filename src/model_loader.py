import logging
from pathlib import Path

import joblib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelLoader:
    # holds my trained artifacts in memory (singleton-ish)
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load()
        return cls._instance

    def _load(self):
        base_path = Path(__file__).parent.parent / "models"
        logger.info("loading model artifacts from %s", base_path)
        self._model = joblib.load(base_path / "model.pkl")
        self._scaler = joblib.load(base_path / "scaler.pkl")
        self._feature_names = joblib.load(base_path / "feature_names.pkl")
        self._label_encoders = joblib.load(base_path / "label_encoders.pkl")

    @property
    def model(self):
        return self._model

    @property
    def scaler(self):
        return self._scaler

    @property
    def feature_names(self):
        return self._feature_names

    @property
    def label_encoders(self):
        return self._label_encoders
