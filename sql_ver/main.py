import streamlit as st
import pandas as pd
import datetime
import pymysql
from sqlalchemy import create_engine
from ui_dashboard import show_dashboard
from ui_result_table import show_results

st.set_page_config(page_title="자동차 리콜 정보 시스템", layout="wide")

# DB 연결 및 데이터 로드
@st.cache_data
def load_data():
    MYSQL_HOSTNAME = 'localhost'
    MYSQL_USER = 'skn14'
    MYSQL_PASSWORD = 'skn14'
    MYSQL_DATABASE = 'skn14_1st_6team'
    connection_string = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOSTNAME}/{MYSQL_DATABASE}'
    db = create_engine(connection_string)

    df = pd.read_sql_table('origin_data', con=db)

    df['prod_period_from'] = pd.to_datetime(df['prod_period_from'], errors='coerce')
    df['prod_period_to'] = pd.to_datetime(df['prod_period_to'], errors='coerce')
    df['recall_start'] = pd.to_datetime(df['recall_start'], errors='coerce')

    df['is_ev'] = df['EV_EV_id'].map({1: '전기차', 2: '내연차'})
    df['is_di'] = df['Domestic_International_DI_id'].map({1: '국내', 2: '해외'})
    df = df.rename(columns={'car_name': 'car', 'recall_reason': 'keyword'})
    df = df.dropna(subset=['prod_period_from', 'prod_period_to'])

    return df

df = load_data()

# 🔥 키워드 리스트 추가
KEYWORD_LIST = [
    "브레이크", "에어백", "연료펌프", "엔진", "전기장치", "조향장치", "타이어",
    "시트벨트", "연료탱크", "배터리", "브레이크 패드", "배기 시스템", "전기 회로",
    "전선 연결", "서스펜션", "속도계", "트랜스미션", "엔진 마운트", "핸들",
    "충격 흡수기", "발전기", "디스크 브레이크", "스파크 플러그", "소음 문제",
    "진동 문제", "냉각 시스템", "연료 시스템", "전장 시스템", "문 열림 문제",
    "헤드램프", "후방 카메라", "내구성 문제", "소프트웨어 버그", "화재 위험",
    "전기 과열", "전기 누전", "스티어링 고장", "부품 결함", "카메라", "소프트웨어", "기타"
]

def extract_keywords_from_description(description):
    """
    리콜 사유(description)에서 키워드를 추출하는 함수
    """
    if pd.isnull(description):
        return ["기타"]
    found_keywords = [keyword for keyword in KEYWORD_LIST if keyword in description]
    return found_keywords if found_keywords else ["기타"]
# UI
# 엔터키 on_change용 함수
def search():
    st.session_state.search_triggered = True

# 세션 상태 초기화
if "search_triggered" not in st.session_state:
    st.session_state.search_triggered = False

# 사이드바 필터
with st.sidebar:
    st.header("🔍 필터 조건")

    search_mode = st.selectbox(
        "검색 방식 선택",
        ["OR 검색", "AND 검색"],
        index=0
    )

    unified_search = st.text_input(
        "제조사 / 차명 / 리콜 사유 통합 검색",
        key="unified_search",
        on_change=search
    )

    is_ev = st.selectbox("차량 유형", ["전체", "전기차", "내연차"])
    is_di = st.selectbox("국내/해외", ["전체", "국내", "해외"])
    prod_date_range = st.date_input("생산 기간 범위", (datetime.date(2000, 1, 1), datetime.date(2024, 12, 31)))

    col1, col2 = st.columns([3, 1])
    with col1:
        reset_button = st.button('초기화')
    with col2:
        search_button = st.button('검색')

filters = {
    "unified_search": st.session_state.get("unified_search", ""),
    "search_mode": search_mode,
    "is_ev": is_ev,
    "is_di": is_di,
    "prod_date_range": prod_date_range
}

# =========================
# 🚗 첫 화면 구성
with st.container():
    st.markdown("<h1 style='text-align: center; font-weight: bold;'>🚗 자동차 리콜 정보 시스템</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; color: gray; font-size: 18px;'>제조사, 차종, 생산 기간 등으로 차량 리콜 이력을 손쉽게 검색하고, 통계까지 한눈에 확인하세요.</p>",
        unsafe_allow_html=True)
    if not (search_button or st.session_state.search_triggered):
        show_dashboard(df)
# =========================

################################ sumilee start #####################################
import os
import urllib.parse
import urllib.request

import requests
from dotenv import load_dotenv
load_dotenv()
import json


# ——— 네이버 Open API 설정 ———
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
NAVER_SEARCH_URL = "https://openapi.naver.com/v1/search/image"

def fetch_naver_image(car_name: str) -> str:
    """
    row['car'] 값으로 '차량명 나무위키' 검색 URL을 직접 만들어
    네이버 Image Search API를 호출하고 첫 번째 이미지를 반환.
    """
    # 1) 검색어 문자열 생성
    query = f"{car_name}"

    # 2) URL 인코딩
    encText = urllib.parse.quote(query)

    url = "https://openapi.naver.com/v1/search/image?query="+encText+"&display=1"
    # 요청 url 등록
    request = urllib.request.Request(url)

    # 요청 header 등록(메타정보)
    request.add_header("X-Naver-Client-Id", NAVER_CLIENT_ID)
    request.add_header("X-Naver-Client-Secret", NAVER_CLIENT_SECRET)

    # try:
    # 5) 요청 보내기
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
        response_json = json.loads(response_body.decode("utf-8"))
        return response_json['items'][0]['link']
    else:
        print("Error Code:" + rescode)
######################### sumilee end ##################################



if search_button or st.session_state.search_triggered:
    filtered_df = df.copy()

    if filters['unified_search']:
        search_words = [word.strip() for word in filters['unified_search'].split(" ") if word.strip()]

        if filters['search_mode'].startswith("OR"):
            # OR 검색: 키워드 중 하나라도 포함
            keyword_condition = False
            for word in search_words:
                keyword_condition = keyword_condition | (
                        filtered_df['company'].str.contains(word, na=False, case=False, regex=False) |
                        filtered_df['car'].str.contains(word, na=False, case=False, regex=False) |
                        filtered_df['keyword'].str.contains(word, na=False, case=False, regex=False)
                )
            filtered_df = filtered_df[keyword_condition]

        elif filters['search_mode'].startswith("AND"):
            # AND 검색: 모든 키워드가 포함되어야 함
            for word in search_words:
                filtered_df = filtered_df[
                    (filtered_df['company'].str.contains(word, na=False, case=False, regex=False)) |
                    (filtered_df['car'].str.contains(word, na=False, case=False, regex=False)) |
                    (filtered_df['keyword'].str.contains(word, na=False, case=False, regex=False))
                    ]

    # 추가 필터링
    if filters['is_ev'] != "전체":
        filtered_df = filtered_df[filtered_df['is_ev'] == filters['is_ev']]

    if filters['is_di'] != "전체":
        filtered_df = filtered_df[filtered_df['is_di'] == filters['is_di']]

    start_date, end_date = filters['prod_date_range']
    if start_date:
        filtered_df = filtered_df[filtered_df['prod_period_from'] >= pd.to_datetime(start_date)]
    if end_date:
        filtered_df = filtered_df[filtered_df['prod_period_to'] <= pd.to_datetime(end_date)]
    # 🔥 리콜 사유에서 키워드 추출해서 새로운 컬럼 추가
    filtered_df['extracted_keywords'] = filtered_df['keyword'].apply(extract_keywords_from_description)
    # 결과 출력
    show_results(filtered_df)

    st.session_state.search_triggered = False

    # 📋 카드 스타일 리콜 상세 결과 추가
    st.subheader("📋 리콜 상세 결과")

    if filtered_df.empty:
        st.warning("검색 결과가 없습니다.")
    else:
        # 같은 차종, 리콜 사유, 제조사로 그룹화 (리콜 날짜는 제외)
        grouped_df = filtered_df.groupby(['company', 'car', 'keyword'])

        for (company, car, keyword), group in grouped_df:
            with st.container():
                st.markdown("---")
                cols = st.columns([1, 4])

                with cols[0]:
                    # 첫 번째 항목에만 이미지 표시
                    car_name = group.iloc[0]['car']
                    img_url = fetch_naver_image(car_name)

                    if img_url:
                        st.image(img_url, width=150)
                    else:
                        st.image("https://via.placeholder.com/150x100.png?text=No+Image", width=150)

                with cols[1]:
                    # 차종, 제조사, 리콜 사유
                    st.markdown(f"### {company} {car}")
                    st.markdown(f"**리콜 사유:** {keyword[:100]}{'...' if len(keyword) > 100 else ''}")

                    # 생산 기간을 나열
                    prod_periods = group[['prod_period_from', 'prod_period_to']].apply(
                        lambda row: f"[{row['prod_period_from'].date()} ~ {row['prod_period_to'].date()}]",
                        axis=1).tolist()
                    st.markdown(f"**생산 기간:** {', '.join(prod_periods)}")

                    # 기타 정보
                    st.markdown(f"**차량 유형:** {group['is_ev'].iloc[0]} / **지역:** {group['is_di'].iloc[0]}")
if search_button or st.session_state.search_triggered:
    # 마지막에 추가
    st.session_state.search_triggered = False

if reset_button:
    st.rerun()
