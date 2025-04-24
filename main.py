import streamlit as st
import datetime

st.set_page_config(page_title="자동차 리콜 정보 시스템", layout="wide")

with st.container():
    st.markdown("""
        <h1 style='text-align: center; color: #2C3E50;'> 자동차 리콜 정보 시스템</h1>
        <p style='text-align: center; color: gray;'>리콜 이력과 통계를 빠르게 검색하고 시각화하는 대시보드입니다.</p>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.header("🔍 필터 조건")

    company = st.text_input("제조사")
    car = st.text_input("차종 검색")
    is_ev = st.selectbox("전기차 여부", ["전체", "전기차", "내연차", "하이브리드"])
    is_di = st.selectbox("국내/해외 여부", ["전체", "국내", "해외"])

    min_date = datetime.date(2000, 1, 1)
    max_date = datetime.date(2025, 12, 31)
    prod_date_range = st.date_input("생산 기간 범위", (datetime.date(2010, 1, 1), datetime.date(2024, 12, 31)), min_value=min_date, max_value=max_date)

    keyword = st.text_input("리콜 사유 키워드")

    col1, col2 = st.columns([3, 1])  # 비율로 너비 설정
    with col2:
        button = st.button('검색')

filters = {
    "company": company,
    "car": car,
    "is_ev": is_ev,
    "is_di": is_di,
    "prod_date_range": prod_date_range,
    "keyword": keyword
}
