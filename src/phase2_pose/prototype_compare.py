"""مقایسه ویژگی‌های حرکتی کاربر با پروتوتایپ‌ها."""

from pathlib import Path
import json
from typing import Dict, Tuple
import numpy as np

PROTO_DIR = Path(__file__).resolve().parent.parent.parent / "models" / "prototypes"

def load_prototype(name: str) -> Dict[str, float]:
    """بارگذاری فایل پروتوتایپ."""
    path = PROTO_DIR / f"{name}.json"
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def compute_similarity(user_feat: Dict[str, float], proto_feat: Dict[str, float]) -> float:
    """محاسبهٔ شباهت معکوس (۱ / (۱ + فاصله)) بین دو مجموعه ویژگی."""
    if not proto_feat:
        return 0.0
    keys = [k for k in user_feat.keys() if k in proto_feat]
    u = np.array([user_feat[k] for k in keys])
    p = np.array([proto_feat[k] for k in keys])
    dist = np.linalg.norm(u - p)
    return float(1.0 / (1.0 + dist))

def compare_to_prototypes(user_feat: Dict[str, float]) -> Dict[str, float]:
    """مقایسه ویژگی‌ها با دو پروتوتایپ پیش‌فرض و بازگشت شباهت آن‌ها."""
    proto1 = load_prototype("proto1_features")
    proto2 = load_prototype("proto2_features")
    sim1 = compute_similarity(user_feat, proto1)
    sim2 = compute_similarity(user_feat, proto2)
    return {"proto1_similarity": sim1, "proto2_similarity": sim2}