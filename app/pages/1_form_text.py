"""صفحه فرم متنی برای فاز اول."""

import os
import sys
from pathlib import Path
import streamlit as st

# افزودن مسیر src به sys.path
BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE_DIR))

from src.core.validators import validate_form
from src.phase1_text.model import predict as predict_phase1
from src.phase1_text.explain import get_feature_contributions
from src.core.config import fuse_confidences

st.set_page_config(page_title="فرم متنی", page_icon="📄", layout="wide")
st.header("فرم متنی - فاز اول")
st.write("اطلاعات زیر را کامل کنید تا سیستم مسیر پیشنهادی شما را در رشته شمشیربازی تعیین کند.")

with st.form("form1"):
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("سن", min_value=10, max_value=60, value=18)
        height_cm = st.number_input("قد (سانتی‌متر)", min_value=100, max_value=220, value=170)
        weight_kg = st.number_input("وزن (کیلوگرم)", min_value=30, max_value=150, value=65)
    with col2:
        dominant_hand = st.selectbox("دست غالب", options=["راست", "چپ"])
        sport_years = st.number_input("سابقه ورزش (سال)", min_value=0, max_value=20, value=1)
        level = st.selectbox("سطح فعلی", options=["مبتدی", "متوسط", "پیشرفته"])
    with col3:
        goal = st.selectbox("هدف", options=["تفریحی", "سلامتی", "مسابقه‌ای"])
        knee_injury = st.slider("آسیب زانو", 0, 3, 0)
        ankle_injury = st.slider("آسیب مچ پا", 0, 3, 0)
        back_injury = st.slider("آسیب کمر", 0, 3, 0)
        shoulder_injury = st.slider("آسیب شانه", 0, 3, 0)
    st.markdown("### تست‌های خودگزارش")
    col4, col5, col6, col7, col8 = st.columns(5)
    with col4:
        reflex = st.slider("رفلکس", 1, 3, 2)
    with col5:
        agility = st.slider("چابکی", 1, 3, 2)
    with col6:
        endurance = st.slider("استقامت", 1, 3, 2)
    with col7:
        explosiveness = st.slider("توان انفجاری", 1, 3, 2)
    with col8:
        stress_tolerance = st.slider("تحمل فشار مسابقه", 1, 3, 2)
    submit = st.form_submit_button("دریافت پیشنهاد")

if submit:
    form_data = {
        "age": age,
        "height_cm": height_cm,
        "weight_kg": weight_kg,
        "dominant_hand": dominant_hand,
        "sport_years": sport_years,
        "level": level,
        "goal": goal,
        "knee_injury": knee_injury,
        "ankle_injury": ankle_injury,
        "back_injury": back_injury,
        "shoulder_injury": shoulder_injury,
        "reflex": reflex,
        "agility": agility,
        "endurance": endurance,
        "explosiveness": explosiveness,
        "stress_tolerance": stress_tolerance,
    }
    result = predict_phase1(form_data)
    if "errors" in result:
        st.error("خطا در ورودی‌ها: " + str(result["errors"]))
    else:
        suggestions = result["suggestions"]
        st.subheader("پیشنهاد مسیر")
        for i, s in enumerate(suggestions):
            if i == 0:
                st.success(f"{i+1}. {s['class']} – اطمینان: {s['confidence']:.2f}")
            else:
                st.info(f"{i+1}. {s['class']} – اطمینان: {s['confidence']:.2f}")
        contribs = get_feature_contributions(form_data, top_k=3)
        with st.expander("توضیح ویژگی‌ها"):
            for cls, feats in contribs.items():
                st.markdown(f"#### {cls}")
                for f in feats:
                    st.markdown(f"* {f['feature']}: مقدار {f['value']}, وزن {f['weight']:+.3f}, تاثیر {f['contribution']:+.3f}")