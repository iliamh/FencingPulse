"""محاسبهٔ ویژگی‌های حرکتی و بیومکانیکی از خروجی ژست."""

from typing import List, Dict
import numpy as np

def summarize_pose_results(results: List[Dict[str, float]]) -> Dict[str, float]:
    """خلاصه‌سازی لیست ویژگی‌های فریم‌ها به چند شاخص.

    پارامتر results: لیستی از دیکشنری که کلیدهای knee_angle, hip_angle, cadence دارند.
    خروجی: دیکشنری شامل میانگین و انحراف معیار هر ویژگی و امتیاز پیشنهادی.
    """
    if not results:
        return {
            "knee_angle_mean": 0.0,
            "knee_angle_std": 0.0,
            "hip_angle_mean": 0.0,
            "hip_angle_std": 0.0,
            "cadence_mean": 0.0,
            "cadence_std": 0.0,
            "pose_score": 0.0
        }
    knee = np.array([r["knee_angle"] for r in results])
    hip = np.array([r["hip_angle"] for r in results])
    cad = np.array([r["cadence"] for r in results])
    summary = {
        "knee_angle_mean": float(knee.mean()),
        "knee_angle_std": float(knee.std()),
        "hip_angle_mean": float(hip.mean()),
        "hip_angle_std": float(hip.std()),
        "cadence_mean": float(cad.mean()),
        "cadence_std": float(cad.std()),
    }
    # امتیاز کلی را بر اساس نزدیکی به محدوده‌های مطلوب محاسبه می‌کنیم
    # محدودهٔ مطلوب برای زاویهٔ زانو 90±15، لگن 90±20، cadence 2±0.5 (ساختگی)
    knee_score = max(0, 1 - abs(summary["knee_angle_mean"] - 90) / 30)
    hip_score = max(0, 1 - abs(summary["hip_angle_mean"] - 90) / 40)
    cad_score = max(0, 1 - abs(summary["cadence_mean"] - 2) / 1.5)
    pose_score = 100 * (0.4 * knee_score + 0.4 * hip_score + 0.2 * cad_score)
    summary["pose_score"] = float(pose_score)
    return summary