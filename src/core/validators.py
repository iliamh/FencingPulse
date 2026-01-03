"""اعتبارسنجی و تبدیل ورودی‌های کاربر."""

from typing import Dict, Any, Tuple

ALLOWED_LEVELS = {"مبتدی", "متوسط", "پیشرفته"}
ALLOWED_GOALS = {"تفریحی", "سلامتی", "مسابقه‌ای"}
ALLOWED_HANDS = {"راست", "چپ"}

def parse_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default

def parse_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default

def validate_form(form: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, str]]:
    """اعتبارسنجی ورودی فرم و تبدیل به انواع مناسب.

    Returns a tuple of (cleaned_data, errors).
    """
    errors: Dict[str, str] = {}
    cleaned: Dict[str, Any] = {}

    # اعداد ساده
    for field in ["age", "height_cm", "weight_kg", "sport_years"]:
        cleaned[field] = parse_float(form.get(field, 0))
        if cleaned[field] < 0:
            errors[field] = "مقدار نمی‌تواند منفی باشد."

    # سطح فعلی
    level = form.get("level", "مبتدی")
    if level not in ALLOWED_LEVELS:
        errors["level"] = "سطح نامعتبر است."
    cleaned["level"] = level

    # هدف
    goal = form.get("goal", "تفریحی")
    if goal not in ALLOWED_GOALS:
        errors["goal"] = "هدف نامعتبر است."
    cleaned["goal"] = goal

    # دست غالب
    hand = form.get("dominant_hand", "راست")
    if hand not in ALLOWED_HANDS:
        errors["dominant_hand"] = "دست غالب نامعتبر است."
    cleaned["dominant_hand"] = hand

    # آسیب‌ها (۰ تا ۳)
    for field in ["knee_injury", "ankle_injury", "back_injury", "shoulder_injury"]:
        cleaned[field] = parse_int(form.get(field, 0))
        if cleaned[field] < 0 or cleaned[field] > 3:
            errors[field] = "شدت باید بین ۰ تا ۳ باشد."

    # تست‌های خودگزارش (۱ تا ۳)
    for field in ["reflex", "agility", "endurance", "explosiveness", "stress_tolerance"]:
        cleaned[field] = parse_int(form.get(field, 1))
        if cleaned[field] < 1 or cleaned[field] > 3:
            errors[field] = "امتیاز باید بین ۱ تا ۳ باشد."

    return cleaned, errors