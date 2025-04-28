import streamlit as st

def show_results(df):
    # 컬럼명 변경 및 필요 작업들
    df = df.rename(columns={
        'company': '제조사',
        'car': '차량모델',
        'prod_period_from': '생산날짜(부터)',
        'prod_period_to': '생산날짜(까지)',
        'recall_start': '리콜날짜',
        'is_ev': '연료타입',
        'is_di': '국내외',
        'keyword' : '리콜사유',
        'extracted_keywords' : '키워드'
    })

    # 'EV_EV_id'와 'Domestic_international_DI_id' 컬럼을 삭제
    df = df.drop(columns=['EV_EV_id', 'Domestic_International_DI_id','keyword_full', 'keyword_short'], errors='ignore')

    # 대시보드 레이아웃
    st.subheader("리콜 상세 내역")

    with st.expander("필터링된 리콜 데이터 보기"):
        st.dataframe(df, use_container_width=True)

    st.caption(f"총 {len(df)}건의 리콜 내역이 검색되었습니다。")

