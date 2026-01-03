"""Video analysis page for phase two.

This page allows users to upload a short fencing video and receive a motion score,
similarity to prototypes, and training recommendations. For full functionality
MediaPipe or MoveNet should be integrated; here we use a simple stub.
"""

import os
import sys
from pathlib import Path
import streamlit as st

# extend sys.path to include project src
BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE_DIR))

from src.phase2_pose.extract_frames import extract_frames
from src.phase2_pose.pose_backend import PoseEstimator
from src.phase2_pose.kinematics import summarize_pose_results
from src.phase2_pose.prototype_compare import compare_to_prototypes
from src.phase2_pose.report_fa import generate_report
from src.core.cache import get_cached_result, set_cached_result

st.set_page_config(page_title="تحلیل ویدئو", layout="wide")
st.header("تحلیل ویدئو (فاز دوم)")
st.write("یک ویدئو کوتاه از حرکات استاندارد شمشیربازی بارگذاری کنید تا سیستم کیفیت حرکتی شما را ارزیابی کند.")

uploaded_file = st.file_uploader("انتخاب ویدئو", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    # save uploaded file to a temporary location
    temp_dir = Path("/tmp/fencingpulse")
    temp_dir.mkdir(exist_ok=True)
    video_path = temp_dir / uploaded_file.name
    with open(video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    cached = get_cached_result(video_path)
    if cached:
        summary = cached.get("summary")
        similarity = cached.get("similarity")
        report = cached.get("report")
    else:
        st.info("در حال پردازش ویدئو… لطفاً کمی صبر کنید.")
        frames = extract_frames(video_path)
        estimator = PoseEstimator()
        results = estimator.process_frames(frames)
        summary = summarize_pose_results(results)
        similarity = compare_to_prototypes(summary)
        report = generate_report(summary, similarity)
        set_cached_result(video_path, {"summary": summary, "similarity": similarity, "report": report})

    st.subheader("امتیاز حرکتی")
    st.metric("امتیاز", f"{summary['pose_score']:.1f} / 100")
    st.write(report["description"])
    st.subheader("توصیه‌های تمرینی")
    for rec in report["recommendations"]:
        st.write("-", rec)
    st.subheader("شباهت به پروتوتایپ‌ها")
    st.write(report["difference_report"])