"""استخراج فریم‌ها از ویدئو برای پردازش ژست.

این ماژول ویدئوی ورودی را باز کرده و فریم‌ها را با نرخ مشخصی استخراج می‌کند.
"""

from typing import List, Tuple
from pathlib import Path
import cv2

def extract_frames(video_path: Path, target_fps: int = 10, max_frames: int = 200) -> List[Tuple[int, any]]:
    """ویدئو را باز کرده و فریم‌ها را بر اساس fps مورد نظر استخراج می‌کند.

    بازگشت: لیستی از زوج (index, frame) که index شماره فریم و frame ماتریس تصویر است.
    """
    if not video_path.exists():
        raise FileNotFoundError(f"ویدئو یافت نشد: {video_path}")
    cap = cv2.VideoCapture(str(video_path))
    frames = []
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    frame_interval = int(max(1, fps // target_fps))
    idx = 0
    while True:
        ret, frame = cap.read()
        if not ret or (max_frames and len(frames) >= max_frames):
            break
        if idx % frame_interval == 0:
            frames.append((idx, frame))
        idx += 1
    cap.release()
    return frames