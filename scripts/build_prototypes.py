#!/usr/bin/env python
"""ساخت پروتوتایپ‌های مرجع از ویدئوهای نمونه."""

import argparse
from pathlib import Path
import json

from src.phase2_pose.extract_frames import extract_frames
from src.phase2_pose.pose_backend import PoseEstimator
from src.phase2_pose.kinematics import summarize_pose_results
from src.core import config

def process_video(video_path: Path) -> dict:
    frames = extract_frames(video_path)
    estimator = PoseEstimator()
    results = estimator.process_frames(frames)
    summary = summarize_pose_results(results)
    return summary

def main(video_paths, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for i, vp in enumerate(video_paths):
        vp_path = Path(vp)
        summary = process_video(vp_path)
        fname = output_dir / f"proto{i+1}_features.json"
        with open(fname, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"Saved prototype {i+1} to {fname}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build prototype features from video")
    parser.add_argument("--input", nargs='+', type=str, help="Paths to input videos")
    parser.add_argument("--output_dir", type=str, default=str(config.get_model_path("prototypes")), help="Output directory for prototypes")
    args = parser.parse_args()
    main(args.input, Path(args.output_dir))