import streamlit as st

def show_results(df):
    st.subheader("📄 리콜 상세 내역")

    with st.expander("🔍 필터링된 리콜 데이터 보기"):
        st.dataframe(df, use_container_width=True)

    st.caption(f"총 {len(df)}건의 리콜 내역이 검색되었습니다。")
