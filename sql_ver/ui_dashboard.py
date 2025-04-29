import streamlit as st
import plotly.express as px
import pandas as pd

def show_dashboard(df):
    st.subheader("리콜 요약")

    # ✅ 전체 데이터 기준으로 요약
    col1, col2, col3 = st.columns(3)
    col1.metric("총 리콜 건수", len(df))
    col2.metric("제조사 수", df['company'].nunique())
    col3.metric("리콜 사유 수", df['keyword'].nunique())

    # 🔥 리콜 사유 분포 (여기는 상위 10개만 사용해도 좋아서 그대로 둬도 됨)
    df['keyword_short'] = df['keyword'].apply(lambda x: x if len(x) <= 15 else x[:15] + "...")

    reason_counts = df['keyword_short'].value_counts().nlargest(10).reset_index()
    reason_counts.columns = ['keyword_short', 'count']

    fig = px.bar(
        reason_counts,
        x='keyword_short',
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
        xaxis_tickangle=-30,
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