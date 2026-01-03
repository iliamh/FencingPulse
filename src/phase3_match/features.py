"""استخراج ویژگی‌ها برای مدل پیش‌بینی نتیجه bout."""

from typing import Dict
import pandas as pd

def build_features(match_data: Dict[str, any]) -> pd.DataFrame:
    """داده bout را به بردار ویژگی تبدیل می‌کند.

    انتظار می‌رود match_data شامل کلیدهای زیر باشد:
      - A_touches_scored_avg
      - A_touches_received_avg
      - B_touches_scored_avg
      - B_touches_received_avg
      - A_fatigue, B_fatigue (۰ تا ۳)
      - A_injury, B_injury (۰ تا ۳)
    """
    features = {}
    # اختلاف میانگین امتیاز گرفته شده و دریافت شده برای هر بازیکن
    a_delta = float(match_data.get("A_touches_scored_avg", 0)) - float(match_data.get("A_touches_received_avg", 0))
    b_delta = float(match_data.get("B_touches_scored_avg", 0)) - float(match_data.get("B_touches_received_avg", 0))
    features["delta_score"] = a_delta - b_delta
    # مجموع امتیازات اخیراً گرفته شده
    features["A_scored"] = float(match_data.get("A_touches_scored_avg", 0))
    features["B_scored"] = float(match_data.get("B_touches_scored_avg", 0))
    # خستگی و آسیب
    features["fatigue_diff"] = float(match_data.get("A_fatigue", 0)) - float(match_data.get("B_fatigue", 0))
    features["injury_diff"] = float(match_data.get("A_injury", 0)) - float(match_data.get("B_injury", 0))
    # می‌توان ویژگی‌های بیشتری اضافه کرد
    return pd.DataFrame([features])