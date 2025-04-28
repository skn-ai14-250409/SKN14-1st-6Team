# import streamlit as st
#
# def show_dashboard(df):
#     st.subheader("리콜 요약")
#
#     col1, col2, col3 = st.columns(3)
#     col1.metric("총 리콜 건수", len(df))
#     col2.metric("제조사 수", df['company'].nunique())
#     col3.metric("사유 수", df['keyword'].nunique())
#
#     st.subheader("리콜 사유 분포 (상위 10개)")
#     reason_counts = df['keyword'].value_counts().head(10)
#     st.bar_chart(reason_counts)


import streamlit as st
import plotly.express as px

def show_dashboard(df):
    st.subheader("🚗 리콜 요약")

    # 1. 리콜 사유 컬럼 두개 준비
    df['keyword_full'] = df['keyword']  # 전체 리콜 사유
    df['keyword_short'] = df['keyword'].apply(lambda x: x[:15] + '...' if len(x) > 15 else x)  # 짧게 요약

    # 2. 상위 10개 리콜 사유만 필터링
    top_keywords = df['keyword'].value_counts().nlargest(10).index.tolist()
    df = df[df['keyword'].isin(top_keywords)]

    col1, col2, col3 = st.columns(3)
    col1.metric("총 리콜 건수", len(df))
    col2.metric("제조사 수", df['company'].nunique())
    col3.metric("리콜 사유 수", df['keyword'].nunique())

    # 마지막 리콜 사유 바 차트
    st.subheader("리콜 사유 분포 (상위 10개)")

    reason_counts = df['keyword'].value_counts().head(10)
    st.bar_chart(reason_counts)

    # 좌우로 나누기
    left_col, right_col = st.columns(2)

    with left_col:
        st.markdown("#### 🚘 연료타입별 리콜 사유 구조 (Sunburst)")

        sunburst_df = df.groupby(['is_ev', 'keyword_short', 'keyword_full']).size().reset_index(name='count')

        fig1 = px.sunburst(
            sunburst_df,
            path=['is_ev', 'keyword_short'],
            values='count',
            width=400,
            height=400
        )

        fig1.update_traces(
            customdata=sunburst_df['keyword_full'],
            hovertemplate='%{customdata}<extra></extra>'
        )

        st.plotly_chart(fig1, use_container_width=True)

    with right_col:
        st.markdown("#### 🏭 상위 제조사별 리콜 사유 (Stacked Bar)")

        top10_companies = df['company'].value_counts().nlargest(10).index.tolist()
        filtered = df[df['company'].isin(top10_companies)]

        bar_df = filtered.groupby(['company', 'keyword_short', 'keyword_full']).size().reset_index(name='count')

        fig2 = px.bar(
            bar_df,
            x='company',
            y='count',
            color='keyword_short',
            title='Top 10 제조사별 리콜 사유 분포',
            barmode='stack',
            width=400,
            height=400
        )

        fig2.update_traces(
            customdata=bar_df['keyword_full'],
            hovertemplate='%{customdata}<extra></extra>'
        )

        st.plotly_chart(fig2, use_container_width=True)