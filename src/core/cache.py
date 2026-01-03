"""ابزار ساده برای ذخیره و بازیابی نتایج پردازش ویدئو.

از این ماژول برای جلوگیری از پردازش تکراری ویدئوهایی که قبلاً بارگذاری شده‌اند استفاده می‌شود. کش بر اساس هش نام فایل و اندازهٔ آن کار می‌کند.
"""

import json
import hashlib
from pathlib import Path
from typing import Any, Optional

# پوشهٔ کش در پوشهٔ models ذخیره می‌شود تا در git نادیده گرفته شود
CACHE_DIR = Path(__file__).resolve().parent.parent / "cache"
CACHE_DIR.mkdir(exist_ok=True)

def _hash_file(path: Path) -> str:
    """محاسبهٔ هش SHA256 یک فایل."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def get_cached_result(video_path: Path) -> Optional[Any]:
    """بررسی اینکه آیا نتیجهٔ پردازش این ویدئو در کش وجود دارد یا نه."""
    if not video_path.exists():
        return None
    key = _hash_file(video_path)
    cache_file = CACHE_DIR / f"{key}.json"
    if cache_file.exists():
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None

def set_cached_result(video_path: Path, result: Any) -> None:
    """ذخیرهٔ نتیجهٔ پردازش ویدئو در کش."""
    key = _hash_file(video_path)
    cache_file = CACHE_DIR / f"{key}.json"
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)