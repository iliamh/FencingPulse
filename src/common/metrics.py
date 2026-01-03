"""پیاده‌سازی سادهٔ معیارهای ارزیابی برای داده‌های طبقه‌بندی."""

import numpy as np
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, log_loss, mean_absolute_error

def accuracy(y_true, y_pred) -> float:
    return float(accuracy_score(y_true, y_pred))

def macro_f1(y_true, y_pred) -> float:
    return float(f1_score(y_true, y_pred, average="macro"))

def auc_score(y_true, y_proba) -> float:
    try:
        return float(roc_auc_score(y_true, y_proba))
    except Exception:
        return 0.0

def logloss(y_true, y_proba) -> float:
    try:
        return float(log_loss(y_true, y_proba))
    except Exception:
        return 0.0

def mae(y_true, y_pred) -> float:
    return float(mean_absolute_error(y_true, y_pred))