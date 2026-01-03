#!/usr/bin/env python
"""آموزش مدل فاز اول بر اساس داده‌های نمونه."""

import argparse
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib

from src.phase1_text.features import extract_features
from src.core import config
from src.phase1_text.model import CLASSES

def main(csv_path: Path, model_output: Path) -> None:
    # خواندن داده‌ها
    df = pd.read_csv(csv_path)
    # تبدیل label به کد عددی بر اساس CLASSES
    label_to_idx = {c: i for i, c in enumerate(CLASSES)}
    y = df["label_weapon"].map(label_to_idx)
    # استخراج ویژگی‌ها
    X_list = []
    for _, row in df.iterrows():
        # تبدیل نام‌به‌نام dict
        cleaned = row.to_dict()
        feats = extract_features(cleaned)
        X_list.append(feats)
    X = pd.concat(X_list, ignore_index=True)
    # آموزش/اعتبارسنجی
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    model = LogisticRegression(max_iter=2000)
    model.fit(X_train, y_train)
    acc = model.score(X_val, y_val)
    print(f"Validation accuracy: {acc:.3f}")
    # ذخیره مدل
    model_output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_output)
    print(f"Model saved to {model_output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train phase 1 model")
    parser.add_argument("--csv", type=str, default="data/sample/phase1_text_sample.csv", help="Path to training CSV")
    parser.add_argument("--output", type=str, default=str(config.get_model_path("phase1_logreg.joblib")), help="Output model file")
    args = parser.parse_args()
    main(Path(args.csv), Path(args.output))