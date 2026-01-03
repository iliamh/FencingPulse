"""توضیح خروجی مدل فاز اول با توجه به ویژگی‌ها."""

from typing import Dict, List
import numpy as np

from .model import load_model, CLASSES
from .features import extract_features
from ..core.validators import validate_form

def get_feature_contributions(form_data: Dict[str, any], top_k: int = 3) -> Dict[str, List[Dict[str, any]]]:
    """سهم هر ویژگی را در تصمیم‌گیری مدل برای هر کلاس برمی‌گرداند.

    خروجی دیکشنری است که برای هر کلاس، فهرست ویژگی‌های با بیشترین اهمیت را دارد.
    """
    cleaned, errors = validate_form(form_data)
    if errors:
        return {"errors": errors}

    X = extract_features(cleaned)
    model = load_model()
    if not hasattr(model, "coef_"):
        return {}
    coef = model.coef_  # شکل: (n_classes, n_features)
    feature_names = list(X.columns)
    contributions = {}
    x_vals = X.values[0]
    # برای هر کلاس بیشترین ضرایب * مقدار ویژگی را می‌گیریم
    for cls_idx, cls_name in enumerate(CLASSES):
        # ارزش هر ویژگی برای این کلاس = ضریب * مقدار ویژگی
        vals = coef[cls_idx] * x_vals
        # مرتب‌سازی نزولی بر اساس قدر مطلق
        indices = np.argsort(np.abs(vals))[::-1]
        top_features = []
        for i in indices[:top_k]:
            top_features.append({
                "feature": feature_names[i],
                "value": float(x_vals[i]),
                "weight": float(coef[cls_idx][i]),
                "contribution": float(vals[i])
            })
        contributions[cls_name] = top_features
    return contributions