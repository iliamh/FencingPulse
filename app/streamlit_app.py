"""اپلیکیشن اصلی Streamlit برای FencingPulse.

این فایل کانفیگ کلی برنامه را تنظیم می‌کند و صفحات را در دایرکتوری `pages/` بارگذاری می‌کند.
برای اجرای برنامه از دستور زیر استفاده کنید:

    streamlit run app/streamlit_app.py
"""

import streamlit as st

st.set_page_config(page_title="FencingPulse", page_icon="🤺", layout="wide")

st.title("سامانهٔ استعداد‌یابی شمشیربازی FencingPulse")
st.write("به سامانهٔ استعداد‌یابی شمشیربازی خوش آمدید. از منوی سمت چپ صفحه مورد نظر را انتخاب کنید.")