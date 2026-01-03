"""پیکربندی‌های اصلی پروژه.

این فایل شامل ثابت‌ها و توابع کمکی برای خواندن پیکربندی‌های سیستم است.
"""

from pathlib import Path

# مسیر پایه پروژه
BASE_DIR = Path(__file__).resolve().parents[2]

# مسیر مدل‌های فازهای مختلف
MODEL_DIR = BASE_DIR / "models"

# وزن‌های پیش‌فرض برای ترکیب اطمینان متن و ویدئو
TEXT_WEIGHT = 0.7
POSE_WEIGHT = 0.3

def get_model_path(model_name: str) -> Path:
    """برگرداندن مسیر مدل آموزش‌دیده."""
    return MODEL_DIR / model_name

def fuse_confidences(conf_text: float, pose_score: float) -> float:
    """وزن‌دهی ساده برای ترکیب اطمینان متنی و امتیاز حرکتی.

    conf_text: احتمال پیش‌بینی‌شده توسط مدل متنی (بین ۰ و ۱)
    pose_score: امتیاز حرکتی (بین ۰ و ۱۰۰)

    خروجی: عدد بین ۰ و ۱
    """
    from math import fmax, fmin
    fused = conf_text * (TEXT_WEIGHT + POSE_WEIGHT * (pose_score / 100.0))
    # محدودسازی به بازهٔ [0, 1]
    return fmin(1.0, fmax(0.0, fused))