"""توابع کمکی برای خواندن و نوشتن داده‌ها."""

from pathlib import Path
from typing import Optional
import pandas as pd

def load_csv(path: Path, **kwargs) -> pd.DataFrame:
    """خواندن فایل CSV با pandas."""
    return pd.read_csv(path, **kwargs)

def save_csv(df: pd.DataFrame, path: Path, **kwargs) -> None:
    """ذخیره DataFrame به CSV."""
    df.to_csv(path, index=False, **kwargs)

def ensure_directory(path: Path) -> None:
    if not path.exists():
        path.mkdir(parents=True)