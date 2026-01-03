#!/usr/bin/env python
"""آموزش مدل فاز سوم بر اساس داده‌های نمونه."""

import argparse
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib

from src.phase3_match.features import build_features
from src.core import config

def main(csv_path: Path, model_output: Path) -> None:
    df = pd.read_csv(csv_path)
    y = df["A_win"].astype(int)
    X_list = []
    for _, row in df.iterrows():
        feats = build_features(row.to_dict())
        X_list.append(feats)
    X = pd.concat(X_list, ignore_index=True)
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)
    acc = model.score(X_val, y_val)
    print(f"Validation accuracy: {acc:.3f}")
    model_output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_output)
    print(f"Model saved to {model_output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train phase 3 model")
    parser.add_argument("--csv", type=str, default="data/sample/phase3_match_sample.csv", help="Path to training CSV")
    parser.add_argument("--output", type=str, default=str(config.get_model_path("phase3_logreg.joblib")), help="Output model file")
    args = parser.parse_args()
    main(Path(args.csv), Path(args.output))