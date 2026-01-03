"""تبدیل داده‌های ورودی فاز اول به ویژگی‌های عددی."""

from typing import Dict
import pandas as pd

HAND_MAP = {"راست": 1, "چپ": 0}
LEVELS = ["مبتدی", "متوسط", "پیشرفته"]
GOALS = ["تفریحی", "سلامتی", "مسابقه‌ای"]

def encode_categorical(value: str, categories: list) -> list:
    """یک دسته را به one-hot encoding تبدیل می‌کند."""
    return [1 if value == cat else 0 for cat in categories]

def extract_features(cleaned: Dict[str, any]) -> pd.DataFrame:
    """دادهٔ فرم تمیز را به بردار ویژگی تبدیل می‌کند و یک DataFrame بازمی‌گرداند."""
    features = {}
    # ویژگی‌های پیوسته
    features["age"] = cleaned.get("age", 0)
    features["height_cm"] = cleaned.get("height_cm", 0)
    features["weight_kg"] = cleaned.get("weight_kg", 0)
    features["sport_years"] = cleaned.get("sport_years", 0)

    # injuries
    features["knee_injury"] = cleaned.get("knee_injury", 0)
    features["ankle_injury"] = cleaned.get("ankle_injury", 0)
    features["back_injury"] = cleaned.get("back_injury", 0)
    features["shoulder_injury"] = cleaned.get("shoulder_injury", 0)

    # self-report tests
    for field in ["reflex", "agility", "endurance", "explosiveness", "stress_tolerance"]:
        features[field] = cleaned.get(field, 1)

    # دست غالب – تبدیل به باینری (راست=1، چپ=0)
    features["dominant_hand_right"] = HAND_MAP.get(cleaned.get("dominant_hand"), 1)

    # one-hot سطح
    level_enc = encode_categorical(cleaned.get("level"), LEVELS)
    for i, lev in enumerate(LEVELS):
        features[f"level_{lev}"] = level_enc[i]

    # one-hot هدف
    goal_enc = encode_categorical(cleaned.get("goal"), GOALS)
    for i, goal in enumerate(GOALS):
        features[f"goal_{goal}"] = goal_enc[i]

    # تبدیل به DataFrame با یک ردیف
    return pd.DataFrame([features])