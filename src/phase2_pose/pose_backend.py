"""پیاده‌سازی سادهٔ تخمین ژست برای فاز دوم.

در این نسخه‌ی نمونه، به دلیل نبود دسترسی به کتابخانه‌های تشخیص ژست، از مقادیر ساختگی برای keypointها استفاده می‌شود. برای کاربرد واقعی باید از MediaPipe یا MoveNet استفاده کنید.
"""

from typing import List, Dict, Any
import random

class PoseEstimator:
    """کلاس نمونه برای تخمین ژست."""
    def __init__(self):
        pass

    def process_frames(self, frames: List[Any]) -> List[Dict[str, float]]:
        """پردازش لیستی از فریم‌ها و برگرداندن ویژگی‌های ساده.

        خروجی: لیستی از دیکشنری که شامل زاویهٔ زانو، زاویهٔ لگن و سرعت تخمینی است.
        """
        results = []
        for idx, frame in frames:
            # تولید مقادیر ساختگی ثابت
            knee_angle = random.uniform(70, 120)  # درجه
            hip_angle = random.uniform(60, 110)
            cadence = random.uniform(1.0, 3.0)  # قدم در ثانیه
            results.append({
                "knee_angle": knee_angle,
                "hip_angle": hip_angle,
                "cadence": cadence
            })
        return results