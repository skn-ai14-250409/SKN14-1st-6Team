import streamlit as st
import plotly.express as px
import pandas as pd

KEYWORD_LIST = [
    "ABS", "ECU", "ESC", "ADAS", "TPMS", "엔진", "변속기", "미션", "배터리", "배터리팩",
    "전기모터", "구동모터", "발전기", "연료펌프", "연료탱크", "연료필터", "연료분사장치",
    "냉각 시스템", "라디에이터", "냉각수", "오일펌프", "히터", "히터코어", "에어컨", "터보차저",
    "흡기매니폴드", "배기관", "배기 시스템", "배출가스장치", "브레이크", "브레이크 패드", "브레이크 오일",
    "디스크 브레이크", "제동등", "시동모터", "플라이휠", "클러치", "차동기어", "구동축", "드라이브샤프트",
    "트랜스미션", "변속레버", "변속기 제어모듈", "전조등", "헤드램프", "후미등", "미등", "주간주행등",
    "사이드미러", "룸미러", "도어락", "도어핸들", "차량도어", "트렁크", "루프", "휀더", "차체프레임", "차체",
    "차량바디", "스티어링 휠", "핸들", "조향기어박스", "조향장치", "파워스티어링", "스티어링 샤프트",
    "충격 흡수기", "서스펜션", "하우징", "샤프트", "기어박스", "차선이탈경고", "차선유지보조", "긴급제동시스템",
    "전방충돌방지장치", "후측방경고", "주차센서", "전방카메라", "후방카메라", "프론트카메라", "센서",
    "거리센서", "속도계", "타이어", "휠", "TPMS 센서", "림", "브레이크 캘리퍼", "브레이크 마스터 실린더",
    "와이어링 하네스", "전장 시스템", "전기 회로", "전선 연결", "전기 과열", "전기 누전", "릴레이", "퓨즈박스",
    "소프트웨어 버그", "소프트웨어 오류", "ECU 소프트웨어", "전기장치", "충전 시스템", "충전 포트", "고압펌프",
    "스파크 플러그", "점화코일", "엔진제어장치", "엔진 마운트", "밸브", "기타 부품 결함", "화재 위험",
    "소음 문제", "진동 문제", "주행 중 시동 꺼짐", "주행 중 전원 차단", "급발진", "감속 불능", "제동 불능",
    "조향 불능", "문 열림 문제", "시트벨트", "에어백", "에어백 전개 불량", "에어백 센서", "헤드레스트",
    "차량시트", "내구성 문제", "차체 강성", "부식 문제", "고장 코드", "통신 오류", "차량 경고등",
    "계기판 오류", "오토라이트", "와이퍼", "와이퍼 모터", "열선시트", "썬루프", "전동시트",
    "자동주차시스템", "어라운드뷰", "블랙박스 오류", "경적 문제", "경고음 미작동", "자동긴급제동 미작동",
    "자동변속기 오류", "수동변속기 오류", "냉각 팬", "엔진 과열", "연료 누출", "오일 누출", "물 유입",
    "방수 불량", "조향 이탈", "조향 고착", "조향 지연", "핸들 떨림", "하체 소음", "서스펜션 이탈",
    "샤시 강성 불량", "차체 균열", "휠 크랙", "타이어 마모 이상", "타이어 공기압 이상", "제동 거리 증가",
    "제동 지연", "주차 브레이크 결함", "시동 불능", "차량 전원 문제", "배터리 과열", "배터리 충전 불량",
    "고전압 시스템", "저전압 시스템", "충전기 결함", "급가속 문제", "변속 충격", "변속 지연", "변속 불능",
    "엔진 소음", "엔진 출력 저하", "냉각수 누수", "히터 불량", "연료 부족 경고 오류", "연료 게이지 오류",
    "트렁크 잠김 불량", "리어게이트 문제", "리어스포일러 문제", "프론트 범퍼 문제", "리어 범퍼 문제",
    "ADAS 센서 오염", "카메라 오류", "라이더 센서 오류", "초음파 센서 오류", "긴급 통신 시스템 문제",
    "내비게이션 오류", "OTA 업데이트 실패", "인포테인먼트 시스템 오류"
]


def extract_keywords_from_description(description):
    """
    리콜 사유(description)에서 키워드를 추출하는 함수
    """
    if pd.isnull(description):
        return ["기타"]
    found_keywords = [keyword for keyword in KEYWORD_LIST if keyword in description]
    return found_keywords


def show_dashboard(df):
    st.subheader("리콜 요약")



    # ✅ 전체 데이터 기준으로 요약
    col1, col2, col3 = st.columns(3)
    col1.metric("총 리콜 건수", len(df))
    col2.metric("제조사 수", df['company'].nunique())
    col3.metric("리콜 사유 수", df['recall_reason'].nunique())

    # 🔥 리콜 사유 분포 (여기는 상위 10개만 사용해도 좋아서 그대로 둬도 됨)
    df['extracted_keywords'] = df['recall_reason'].apply(extract_keywords_from_description)
    # df['extracted_keywords'] = df['extracted_keywords'].apply(lambda x: x if len(x) <= 15 else x[:15] + "...")


    reason_counts = df.explode('extracted_keywords')['extracted_keywords'].value_counts().nlargest(10).reset_index()
    reason_counts.columns = ['extracted_keywords', 'count']

    fig = px.bar(
        reason_counts,
        x='extracted_keywords',
        y='count',
        text='count',
        title='리콜 사유 분포 (상위 10개)'
    )

    # ✨ Hover 텍스트를 커스텀: 리콜 사유 내용만 뜨게
    fig.update_traces(
        hovertemplate="%{x}<extra></extra>",  # x축 값만 보여주고, extra(기타 정보) 숨김
        textposition='outside'
    )
    # ✨ Layout 설정
    fig.update_layout(
        xaxis_title="리콜 사유",
        yaxis_title="건수",
        title_x=0.5
    )
    st.plotly_chart(fig, use_container_width=True)

    cols = st.columns(2)
    with cols[0]:
        # 1. 생산 시작 연도(prod_period_from) 컬럼 생성
        df['prod_year'] = df['prod_period_from'].dt.year

        # 2. 생산 시작 연도별 리콜 건수 집계
        yearly_counts = df.groupby('prod_year').size().reset_index(name='count')

        # 3. 2000~2024년까지 모든 연도 리스트 만들기
        all_years = pd.DataFrame({'prod_year': list(range(2000, 2025))})

        yearly_counts = pd.merge(all_years, yearly_counts, on='prod_year', how='left').fillna(0)
        yearly_counts['count'] = yearly_counts['count'].astype(int)

        fig1 = px.line(
            yearly_counts,
            x='prod_year',
            y='count',
            markers=True,
            title='생산 시작 연도별 리콜 건수 변화'
        )
        st.plotly_chart(fig1, use_container_width=True)

    with cols[1]:
        # 2. 추가 : 제조사별 리콜 비율
        top_companies = df['company'].value_counts().nlargest(10)
        fig2 = px.pie(values=top_companies.values, names=top_companies.index, title='제조사별 리콜 비율')
        st.plotly_chart(fig2, use_container_width=True)