# import streamlit as st
# import pandas as pd
# import datetime
# from ui_dashboard import show_dashboard
# from ui_result_table import show_results
#
# st.set_page_config(page_title="자동차 리콜 정보 시스템", layout="wide")
#
# #  전기차/하이브리드/내연차 구분 함수
# def classify_ev_type(car_name):
#     car_name = str(car_name).lower()
#     if any(ev in car_name for ev in ['ev', '아이오닉', '모델', 'ix', 'eq', 'bolt', 'leaf']): # 리스트 안 이름이 포함됐을 경우 전기차를 리턴
#         return '전기차'
#     elif any(hv in car_name for hv in ['hev', '하이브리드', 'hybrid', 'phev']): # 리스트 안 이름이 포함됐을 경우 하이브리드 리턴
#         return '하이브리드'
#     else:
#         return '내연차'
#
# # 데이터 로드 및 전처리 함수
# @st.cache_data
# def load_data():
#     df = pd.read_csv("한국교통안전공단_자동차결함 리콜현황_20231231.csv", encoding='cp949')
#     df.rename(columns={
#         '제작자': 'company',
#         '차명': 'car',
#         '생산기간(부터)': 'start_date',
#         '생산기간(까지)': 'end_date',
#         '리콜사유': 'keyword'
#     }, inplace=True)
#     df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce')
#     df['end_date'] = pd.to_datetime(df['end_date'], errors='coerce')
#     df['is_ev'] = df['car'].apply(classify_ev_type)
#     df['is_di'] = df['company'].apply(lambda x: '국내' if '현대' in x or '기아' in x else '해외')
#     return df
#
# df = load_data()
#
# # 💡 UI 설정
# with st.container(): # 그냥 설명창
#     st.markdown("""
#         <h1 style='text-align: center; color: #2C3E50;'> 자동차 리콜 정보 시스템</h1>
#         <p style='text-align: center; color: gray;'>리콜 이력과 통계를 빠르게 검색하고 시각화하는 대시보드입니다.</p>
#     """, unsafe_allow_html=True)
#
# with st.sidebar: # 사이드바
#     st.header("🔍 필터 조건") # 이름
#
#     company = st.text_input("제조사") # 회사 검색창
#     car = st.text_input("차종 검색") # 차종을 검색창
#     is_ev = st.selectbox("전기차 여부", ["전체", "전기차", "하이브리드", "내연차"]) # 차량 운행 방식 선택창
#     is_di = st.selectbox("국내/해외 여부", ["전체", "국내", "해외"]) # 국내 해외 선택창
#
#     min_date = datetime.date(2000, 1, 1) # 최소 날짜
#     max_date = datetime.date(2024, 12, 31) # 최소 날짜
#     prod_date_range = st.date_input("생산 기간 범위", (datetime.date(2010, 1, 1), datetime.date(2024, 12, 31)), min_value=min_date, max_value=max_date)
#     # prod_date_range에 datetime.date 객체가 튜플 형식으로 저장된 후 prod_date_range 변수 안에 저장됨
#
#     keyword = st.text_input("리콜 사유 키워드") # 키워드 검색창
#
#     col1, col2 = st.columns([2, 1]) # 검색과 초기화 버튼 위치 조정 코드
#     with col1:
#         search_button = st.button('검색')
#     with col2:
#         reset_button = st.button('초기화') # 아직 미완성
#
# # 🎯 필터링 조건
# filters = {
#     "company": company,(
#     "car": car,
#     "is_ev": is_ev,
#     "is_di": is_di,
#     "prod_date_range": prod_date_range,
#     "keyword": keyword
# }
#
# # 검색 버튼 동작 이건 한 번에 하나밖에 필터링 못함
# # 대충 입력 내용이 포함됐으면 전부 가져오도록 해주는 코드, 필터링 코드
# # ... (위 코드는 그대로 유지됨)
#
# # 🔍 검색 버튼 동작
# if search_button:
#     filtered_df = df.copy()
#
#     if filters['company']:
#         filtered_df = filtered_df[filtered_df['company'].str.contains(filters['company'], na=False)]
#
#     if filters['car']:
#         filtered_df = filtered_df[filtered_df['car'].str.contains(filters['car'], na=False)]
#
#     if filters['is_ev'] != "전체":
#         filtered_df = filtered_df[filtered_df['is_ev'] == filters['is_ev']]
#
#     if filters['is_di'] != "전체":
#         filtered_df = filtered_df[filtered_df['is_di'] == filters['is_di']]
#
#     start_date, end_date = filters['prod_date_range']
#     filtered_df = filtered_df[
#         (filtered_df['start_date'] >= pd.to_datetime(start_date)) &
#         (filtered_df['end_date'] <= pd.to_datetime(end_date))
#     ]
#
#     if filters['keyword']:
#         filtered_df = filtered_df[filtered_df['keyword'].str.contains(filters['keyword'], na=False)]
#
#     # 📊 대시보드 시각화
#     show_dashboard(filtered_df)
#
#     # 🧾 카드 형식 검색 결과 표시
#     st.subheader("📋 리콜 상세 결과")
#
#     if filtered_df.empty:
#         st.warning("검색 결과가 없습니다.")
#     else:
#         for i, row in filtered_df.iterrows():
#             with st.container():
#                 st.markdown("---")
#                 cols = st.columns([1, 4])
#
#                 with cols[0]:
#                     st.image("https://via.placeholder.com/150x100.png?text=No+Image", width=150)
#
#                 with cols[1]:
#                     st.markdown(f"### {row['company']} {row['car']}")
#                     st.markdown(f" **리콜 사유:** {row['keyword'][:100]}{'...' if len(row['keyword']) > 100 else ''}")
#                     st.markdown(f" **생산 기간:** {row['start_date'].date()} ~ {row['end_date'].date()}")
#                     st.markdown(f" **차량 유형:** {row['is_ev']}  /   **지역:** {row['is_di']}")
#
#
# if reset_button:
#     st.rerun()
#


##### 최종_1 ####
# import streamlit as st
# import pandas as pd
# import datetime
# import pymysql
# from sqlalchemy import create_engine
# from ui_dashboard import show_dashboard
# from ui_result_table import show_results
#
# st.set_page_config(page_title="자동차 리콜 정보 시스템", layout="wide")
#
# # DB 연결 및 데이터 로드
# @st.cache_data
# def load_data():
#     MYSQL_HOSTNAME = 'localhost'
#     MYSQL_USER = 'skn14'
#     MYSQL_PASSWORD = 'skn14'
#     MYSQL_DATABASE = 'skn14_1st_6team'
#     connection_string = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOSTNAME}/{MYSQL_DATABASE}'
#     db = create_engine(connection_string)
#
#     df = pd.read_sql_table('origin_data', con=db)
#
#     df['prod_period_from'] = pd.to_datetime(df['prod_period_from'], errors='coerce')
#     df['prod_period_to'] = pd.to_datetime(df['prod_period_to'], errors='coerce')
#     df['recall_start'] = pd.to_datetime(df['recall_start'], errors='coerce')
#
#     df['is_ev'] = df['EV_EV_id'].map({1: '전기차', 2: '내연차'})
#     df['is_di'] = df['Domestic_International_DI_id'].map({1: '국내', 2: '해외'})
#     df = df.rename(columns={'car_name': 'car', 'recall_reason': 'keyword'})
#     df = df.dropna(subset=['prod_period_from', 'prod_period_to'])
#
#     return df
#
# df = load_data()
#
# # UI
# with st.container():
#     st.markdown("""
#         <h1 style='text-align: center;'>자동차 리콜 정보 시스템</h1>
#         <p style='text-align: center; color: gray;'>MySQL에 저장된 리콜 이력과 통계를 조회합니다.</p>
#     """, unsafe_allow_html=True)
#
# with st.sidebar:
#     st.header("🔍 필터 조건")
#     company = st.text_input("제조사")
#     car = st.text_input("차종")
#     is_ev = st.selectbox("차량 유형", ["전체", "전기차", "내연차"])
#     is_di = st.selectbox("국내/해외", ["전체", "국내", "해외"])
#     prod_date_range = st.date_input("생산 기간 범위", (datetime.date(2010, 1, 1), datetime.date(2024, 12, 31)))
#     keyword = st.text_input("리콜 사유 키워드")
#
#     col1, col2 = st.columns([2, 1])
#     with col1:
#         search_button = st.button('검색')
#     with col2:
#         reset_button = st.button('초기화')
#
# filters = {
#     "company": company,
#     "car": car,
#     "is_ev": is_ev,
#     "is_di": is_di,
#     "prod_date_range": prod_date_range,
#     "keyword": keyword
# }
#
# if search_button:
#     filtered_df = df.copy()
#
#     if filters['company']:
#         filtered_df = filtered_df[filtered_df['company'].str.contains(filters['company'], na=False)]
#
#     if filters['car']:
#         filtered_df = filtered_df[filtered_df['car'].str.contains(filters['car'], na=False)]
#
#     if filters['is_ev'] != "전체":
#         filtered_df = filtered_df[filtered_df['is_ev'] == filters['is_ev']]
#
#     if filters['is_di'] != "전체":
#         filtered_df = filtered_df[filtered_df['is_di'] == filters['is_di']]
#
#     start_date, end_date = filters['prod_date_range']
#     filtered_df = filtered_df[
#         (filtered_df['prod_period_from'] >= pd.to_datetime(start_date)) &
#         (filtered_df['prod_period_to'] <= pd.to_datetime(end_date))
#     ]
#
#     if filters['keyword']:
#         filtered_df = filtered_df[filtered_df['keyword'].str.contains(filters['keyword'], na=False)]
#
#     show_dashboard(filtered_df)
#     show_results(filtered_df)
#
# if reset_button:
#     st.rerun()










import streamlit as st
import pandas as pd
import datetime
from ui_dashboard import show_dashboard
from ui_result_table import show_results

st.set_page_config(page_title="자동차 리콜 정보 시스템", layout="wide")

#  전기차/하이브리드/내연차 구분 함수
def classify_ev_type(car_name):
    car_name = str(car_name).lower()
    if any(ev in car_name for ev in ['ev', '아이오닉', '모델', 'ix', 'eq', 'bolt', 'leaf']): # 리스트 안 이름이 포함됐을 경우 전기차를 리턴
        return '전기차'
    elif any(hv in car_name for hv in ['hev', '하이브리드', 'hybrid', 'phev']): # 리스트 안 이름이 포함됐을 경우 하이브리드 리턴
        return '하이브리드'
    else:
        return '내연차'

# 데이터 로드 및 전처리 함수
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

# 💡 UI 설정
with st.container(): # 그냥 설명창
    st.markdown("""
        <h1 style='text-align: center; color: #2C3E50;'> 자동차 리콜 정보 시스템</h1>
        <p style='text-align: center; color: gray;'>리콜 이력과 통계를 빠르게 검색하고 시각화하는 대시보드입니다.</p>
    """, unsafe_allow_html=True)

with st.sidebar: # 사이드바
    st.header("🔍 필터 조건") # 이름

    company = st.text_input("제조사") # 회사 검색창
    car = st.text_input("차종 검색") # 차종을 검색창
    is_ev = st.selectbox("전기차 여부", ["전체", "전기차", "하이브리드", "내연차"]) # 차량 운행 방식 선택창
    is_di = st.selectbox("국내/해외 여부", ["전체", "국내", "해외"]) # 국내 해외 선택창

    min_date = datetime.date(2000, 1, 1) # 최소 날짜
    max_date = datetime.date(2024, 12, 31) # 최소 날짜
    prod_date_range = st.date_input("생산 기간 범위", (datetime.date(2010, 1, 1), datetime.date(2024, 12, 31)), min_value=min_date, max_value=max_date)
    # prod_date_range에 datetime.date 객체가 튜플 형식으로 저장된 후 prod_date_range 변수 안에 저장됨

    keyword = st.text_input("리콜 사유 키워드") # 키워드 검색창

    col1, col2 = st.columns([2, 1]) # 검색과 초기화 버튼 위치 조정 코드
    with col1:
        search_button = st.button('검색')
    with col2:
        reset_button = st.button('초기화') # 아직 미완성

# 🎯 필터링 조건
filters = {
    "company": company,
    "car": car,
    "is_ev": is_ev,
    "is_di": is_di,
    "prod_date_range": prod_date_range,
    "keyword": keyword
}

# 검색 버튼 동작 이건 한 번에 하나밖에 필터링 못함
# 대충 입력 내용이 포함됐으면 전부 가져오도록 해주는 코드, 필터링 코드
# ... (위 코드는 그대로 유지됨)

# 🔍 검색 버튼 동작
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

    # 📊 대시보드 시각화
    show_dashboard(filtered_df)

    # 🧾 카드 형식 검색 결과 표시
    st.subheader("📋 리콜 상세 결과")

    if filtered_df.empty:
        st.warning("검색 결과가 없습니다.")
    else:
        for i, row in filtered_df.iterrows():
            with st.container():
                st.markdown("---")
                cols = st.columns([1, 4])

                with cols[0]:
                    st.image("https://via.placeholder.com/150x100.png?text=No+Image", width=150)

                with cols[1]:
                    st.markdown(f"### {row['company']} {row['car']}")
                    st.markdown(f" **리콜 사유:** {row['keyword'][:100]}{'...' if len(row['keyword']) > 100 else ''}")
                    st.markdown(f" **생산 기간:** {row['start_date'].date()} ~ {row['end_date'].date()}")
                    st.markdown(f" **차량 유형:** {row['is_ev']}  /   **지역:** {row['is_di']}")


if reset_button:
    st.rerun()





