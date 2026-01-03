"""توضیح مدل فاز سوم و ویژگی‌های مؤثر در پیش‌بینی."""

from typing import Dict, List
import numpy as np

from .model import load_model
from .features import build_features

def get_feature_contributions(match_data: Dict[str, any], top_k: int = 3) -> List[Dict[str, any]]:
    """بازگرداندن لیست ویژگی‌های تأثیرگذار همراه با وزن و مقدار برای کلاس برد A."""
    X = build_features(match_data)
    model = load_model()
    if not hasattr(model, "coef_"):
        return []
    coef = model.coef_[0]  # فرض می‌کنیم مدل باینری است
    feature_names = list(X.columns)
    vals = coef * X.values[0]
    indices = np.argsort(np.abs(vals))[::-1]
    contributions = []
    for i in indices[:top_k]:
        contributions.append({
            "feature": feature_names[i],
            "value": float(X.values[0][i]),
            "weight": float(coef[i]),
            "contribution": float(vals[i])
        })
    return contributions