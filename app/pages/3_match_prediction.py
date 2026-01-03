"""صفحه پیش‌بینی نتیجه مسابقه (فاز سوم)."""

import os
import sys
from pathlib import Path
import streamlit as st

BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE_DIR))

from src.phase3_match.model import predict as predict_match
from src.phase3_match.explain import get_feature_contributions
from src.phase3_match.features import build_features

st.set_page_config(page_title="پیش‌بینی مسابقه", layout="wide")
st.header("پیش‌بینی مسابقه - فاز سوم")
st.write("اطلاعات خلاصه bout بین دو شمشیرباز را وارد کنید تا احتمال برد بازیکن A محاسبه شود.")

with st.form("match_form"):
    st.markdown("### میانگین امتیازات A")
    a_scored = st.number_input("A - میانگین امتیازات گرفته", min_value=0.0, max_value=10.0, value=5.0)
    a_received = st.number_input("A - میانگین امتیازات دریافت‌شده", min_value=0.0, max_value=10.0, value=5.0)
    st.markdown("### میانگین امتیازات B")
    b_scored = st.number_input("B - میانگین امتیازات گرفته", min_value=0.0, max_value=10.0, value=5.0)
    b_received = st.number_input("B - میانگین امتیازات دریافت‌شده", min_value=0.0, max_value=10.0, value=5.0)
    st.markdown("### خستگی و آسیب")
    a_fatigue = st.slider("A - خستگی", 0, 3, 1)
    b_fatigue = st.slider("B - خستگی", 0, 3, 1)
    a_injury = st.slider("A - آسیب", 0, 3, 0)
    b_injury = st.slider("B - آسیب", 0, 3, 0)
    submit_match = st.form_submit_button("پیش‌بینی")

if submit_match:
    match_data = {
        "A_touches_scored_avg": a_scored,
        "A_touches_received_avg": a_received,
        "B_touches_scored_avg": b_scored,
        "B_touches_received_avg": b_received,
        "A_fatigue": a_fatigue,
        "B_fatigue": b_fatigue,
        "A_injury": a_injury,
        "B_injury": b_injury,
    }
    result = predict_match(match_data)
    st.subheader("احتمال برد")
    st.write(f"احتمال برد A: {result['probability_A_win']:.2f}")
    st.write(f"احتمال برد B: {result['probability_B_win']:.2f}")
    contribs = get_feature_contributions(match_data, top_k=3)
    st.subheader("ویژگی‌های مؤثر")
    for f in contribs:
        st.write(f"- {f['feature']}: مقدار {f['value']}, وزن {f['weight']:+.3f}, تاثیر {f['contribution']:+.3f}")