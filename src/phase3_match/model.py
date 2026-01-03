"""مدل و توابع پیش‌بینی برای فاز سوم (نتیجه مسابقه)."""

from pathlib import Path
from typing import Dict
import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression

from ..core import config
from .features import build_features

MODEL_PATH = config.get_model_path("phase3_logreg.joblib")

_model = None

def load_model() -> LogisticRegression:
    global _model
    if _model is not None:
        return _model
    if MODEL_PATH.exists():
        _model = joblib.load(MODEL_PATH)
    else:
        _model = LogisticRegression(max_iter=100)
        # dummy training
        X = np.zeros((2, 3))
        y = np.array([0, 1])
        try:
            _model.fit(X, y)
        except Exception:
            pass
    return _model

def predict(match_data: Dict[str, any]) -> Dict[str, any]:
    """پیش‌بینی احتمال برد بازیکن A بر اساس داده bout."""
    X = build_features(match_data)
    model = load_model()
    try:
        prob = model.predict_proba(X)[0]
    except Exception:
        prob = np.array([0.5, 0.5])
    return {
        "probability_A_win": float(prob[1]),
        "probability_B_win": float(prob[0])
    }