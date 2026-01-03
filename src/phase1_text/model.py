"""مدل و توابع پیش‌بینی برای فاز اول (پیشنهاد مسیر شمشیربازی)."""

from pathlib import Path
from typing import Tuple, List, Dict
import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression

from ..core import config
from ..common.io import load_csv
from .features import extract_features

MODEL_PATH = config.get_model_path("phase1_logreg.joblib")

CLASSES = ["فلوره", "اپه", "سابر"]  # ترتیب کلاس‌ها در مدل

_model = None

def load_model() -> LogisticRegression:
    """بارگذاری مدل آموزش‌دیده از فایل. اگر وجود نداشته باشد، مدل اولیه ساخته می‌شود."""
    global _model
    if _model is not None:
        return _model
    if MODEL_PATH.exists():
        _model = joblib.load(MODEL_PATH)
    else:
        # مدل پیش‌فرض با پارامترهای پایه و بدون آموزش، تا خطا رخ ندهد
        _model = LogisticRegression(max_iter=2000)
        # fitting with dummy data so that coef_ exists
        X = np.zeros((len(CLASSES), 3))
        y = np.array(range(len(CLASSES)))
        try:
            _model.fit(X, y)
        except Exception:
            pass
    return _model

def predict(form_data: Dict[str, any]) -> Dict[str, any]:
    """دادهٔ فرم را گرفته و خروجی مدل به همراه اطمینان و توضیح را برمی‌گرداند.

    خروجی شامل موارد زیر است:
      - suggestion: فهرست پیشنهادها و احتمال‌ها
    """
    from ..core.validators import validate_form
    cleaned, errors = validate_form(form_data)
    if errors:
        return {"errors": errors}
    X = extract_features(cleaned)
    model = load_model()
    try:
        proba = model.predict_proba(X)[0]
    except Exception:
        # اگر مدل درست آموزش ندیده، احتمال‌ها را مساوی فرض کن
        proba = np.ones(len(CLASSES)) / len(CLASSES)
    # مرتب‌سازی بر اساس احتمال نزولی
    idx_sorted = np.argsort(proba)[::-1]
    suggestions = []
    for idx in idx_sorted:
        suggestions.append({
            "class": CLASSES[idx],
            "confidence": float(proba[idx])
        })
    return {
        "suggestions": suggestions,
        "cleaned_data": cleaned
    }