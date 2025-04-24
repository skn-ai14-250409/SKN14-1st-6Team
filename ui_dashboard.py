import streamlit as st

def show_dashboard(df):
    st.subheader("📊 리콜 요약")

    col1, col2, col3 = st.columns(3)
    col1.metric("총 리콜 건수", len(df))
    col2.metric("제조사 수", df['company'].nunique())
    col3.metric("사유 수", df['keyword'].nunique())

    st.subheader("리콜 사유 분포 (상위 10개)")
    reason_counts = df['keyword'].value_counts().head(10)
    st.bar_chart(reason_counts)