import streamlit as st
import pandas as pd
import datetime
from ui_dashboard import show_dashboard
from ui_result_table import show_results

st.set_page_config(page_title="자동차 리콜 정보 시스템", layout="wide")

# 🔧 전기차/하이브리드/내연차 구분 함수
def classify_ev_type(car_name):
    car_name = str(car_name).lower()
    if any(ev in car_name for ev in ['ev', '아이오닉', '모델', 'ix', 'eq', 'bolt', 'leaf']):
        return '전기차'
    elif any(hv in car_name for hv in ['hev', '하이브리드', 'hybrid', 'phev']):
        return '하이브리드'
    else:
        return '내연차'

# 📅 날짜 보정 함수
def normalize_date_range(date_range, min_date, max_date):
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start, end = date_range

        if start and not end:
            return (start, max_date)
        elif end and not start:
            return (min_date, end)
        elif start > end:
            return (end, start)
        else:
            return (start, end)

    return (min_date, max_date)

# 📄 CSV 로드
@st.cache_data
def load_data():
    df = pd.read_csv("한국교통안전공단_자동차결함 리콜현황_20231231.csv", encoding='cp949')
    df.rename(columns={
        '제작자': 'company',
        '차명': 'car',
        '생산기간(부터)': 'start_date',
        '생산기간(까지)': 'end_date',
        '리콜사유': 'keyword'
    }, inplace=True)
    df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce')
    df['end_date'] = pd.to_datetime(df['end_date'], errors='coerce')
    df['is_ev'] = df['car'].apply(classify_ev_type)
    df['is_di'] = df['company'].apply(lambda x: '국내' if '현대' in x or '기아' in x else '해외')
    return df

df = load_data()

# 🖥️ 메인 UI
with st.container():
    st.markdown("""
        <h1 style='text-align: center; color: #2C3E50;'> 자동차 리콜 정보 시스템</h1>
        <p style='text-align: center; color: gray;'>리콜 이력과 통계를 빠르게 검색하고 시각화하는 대시보드입니다.</p>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.header("🔍 필터 조건")

    company = st.text_input("제조사")
    car = st.text_input("차종 검색")
    is_ev = st.selectbox("전기차 여부", ["전체", "전기차", "하이브리드", "내연차"])
    is_di = st.selectbox("국내/해외 여부", ["전체", "국내", "해외"])

    min_date = datetime.date(2000, 1, 1)
    max_date = datetime.date(2024, 12, 31)
    prod_date_range = st.date_input(
        "생산 기간 범위",
        (datetime.date(2010, 1, 1), datetime.date(2024, 12, 31)),
        min_value=min_date,
        max_value=max_date
    )

    keyword = st.text_input("리콜 사유 키워드")

    col1, col2 = st.columns([2, 1])
    with col1:
        search_button = st.button('🔎 Explore')
    with col2:
        reset_button = st.button('🔄 Reset')

# 🎯 날짜 범위 보정
prod_date_range = normalize_date_range(prod_date_range, min_date, max_date)

# 필터 저장
filters = {
    "company": company,
    "car": car,
    "is_ev": is_ev,
    "is_di": is_di,
    "prod_date_range": prod_date_range,
    "keyword": keyword
}

# 🔍 검색 버튼 눌렀을 때
if search_button:
    filtered_df = df.copy()

    if filters['company']:
        filtered_df = filtered_df[filtered_df['company'].str.contains(filters['company'], na=False)]

    if filters['car']:
        filtered_df = filtered_df[filtered_df['car'].str.contains(filters['car'], na=False)]

    if filters['is_ev'] != "전체":
        filtered_df = filtered_df[filtered_df['is_ev'] == filters['is_ev']]

    if filters['is_di'] != "전체":
        filtered_df = filtered_df[filtered_df['is_di'] == filters['is_di']]

    start_date, end_date = filters['prod_date_range']
    filtered_df = filtered_df[
        (filtered_df['start_date'] >= pd.to_datetime(start_date)) &
        (filtered_df['end_date'] <= pd.to_datetime(end_date))
    ]

    if filters['keyword']:
        filtered_df = filtered_df[filtered_df['keyword'].str.contains(filters['keyword'], na=False)]

    show_dashboard(filtered_df)
    show_results(filtered_df)

# 🔄 초기화 버튼 눌렀을 때
if reset_button:
    st.session_state.clear()
    st.rerun()
