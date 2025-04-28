# import pymysql
# from sqlalchemy import create_engine
# import pandas as pd
#
# MYSQL_HOSTNAME = 'localhost' # you probably don't need to change this
# # MYSQL_USER = 'root'
# # MYSQL_PASSWORD = 'mysql'
# # MYSQL_DATABASE = 'skn14_1st_6team'
# MYSQL_USER = 'skn14'
# MYSQL_PASSWORD = 'skn14'
# MYSQL_DATABASE = 'skn14_1st_6team'
#
# connection_string = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOSTNAME}/{MYSQL_DATABASE}'
# connect_args = {'ssl': {'ca': '/content/rds-ca-2015-root.pem'}}
# db = create_engine(connection_string)
#
# df = pd.read_csv('한국교통안전공단_자동차결함 리콜현황_20231231.csv', encoding='cp949')
#
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
#
#
# def is_ev(car_name, reason):
#     ev_keywords = ['ev', 'EV', '아이오닉', 'iX', '전기', '하이브리드', 'Hybrid', '전동']
#     text = f"{car_name} {reason}".lower()
#     return 1 if any(k.lower() in text for k in ev_keywords) else 2
#
# def is_domestic(maker):
#     domestic_makers = ['현대', '기아', '쌍용', '르노', '쉐보레', '한국GM', '대우']
#     return 1 if any(dom in maker for dom in domestic_makers) else 2
#
# df['EV_EV_id'] = df.apply(lambda row: is_ev(row['차명'], row['리콜사유']), axis=1)
# df['Domestic_International_DI_id'] = df['제작자'].apply(is_domestic)
#
#
#
# #컬럼명 변경
# df_cleaned = df.rename(columns={
#     '제작자': 'company',
#     '생산기간(부터)': 'prod_period_from',
#     '생산기간(까지)': 'prod_period_to',
#     '리콜개시일': 'recall_start',
#     '리콜사유': 'recall_reason'
# })[['company', 'prod_period_from', 'prod_period_to', 'recall_start', 'recall_reason', 'EV_EV_id', 'Domestic_International_DI_id']]
#
#
# #날짜 컬럼 형식 변환
# df_cleaned['prod_period_from'] = pd.to_datetime(df_cleaned['prod_period_from'], errors='coerce')
# df_cleaned['prod_period_to'] = pd.to_datetime(df_cleaned['prod_period_to'], errors='coerce')
# df_cleaned['recall_start'] = pd.to_datetime(df_cleaned['recall_start'], errors='coerce')
#
# df.to_sql(con=db, name='recall_current', if_exists='append', index=False)
# print("✅ MySQL DB에 데이터 삽입 완료")



import pymysql
from sqlalchemy import create_engine
import pandas as pd

# MySQL 연결 설정
MYSQL_HOSTNAME = 'localhost'
MYSQL_USER = 'skn14'
MYSQL_PASSWORD = 'skn14'
MYSQL_DATABASE = 'skn14_1st_6team'


connection_string = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOSTNAME}/{MYSQL_DATABASE}'
db = create_engine(connection_string)

# CSV 파일 읽기
df = pd.read_csv('../한국교통안전공단_자동차결함 리콜현황_20231231.csv', encoding='cp949')

# 컬럼명 영어로 변경
df = df.rename(columns={
    '제작자': 'company',
    '차명': 'car_name',
    '생산기간(부터)': 'prod_period_from',
    '생산기간(까지)': 'prod_period_to',
    '리콜개시일': 'recall_start',
    '리콜사유': 'recall_reason'
})
# 전기차/국내 여부 추가 ✨
def is_ev(car_name, reason):
    ev_keywords = ['ev', 'EV', '아이오닉', 'iX', '전기', '하이브리드', 'Hybrid', '전동']
    text = f"{car_name} {reason}".lower()
    return 1 if any(k.lower() in text for k in ev_keywords) else 2

def is_domestic(maker):
    domestic_makers = ['현대', '기아', '쌍용', '르노', '쉐보레', '한국GM', '대우']
    return 1 if any(dom in maker for dom in domestic_makers) else 2

df['EV_EV_id'] = df.apply(lambda row: is_ev(row['car_name'], row['recall_reason']), axis=1)
df['Domestic_International_DI_id'] = df['company'].apply(is_domestic)

# 날짜 컬럼 타입 변환
df['prod_period_from'] = pd.to_datetime(df['prod_period_from'], errors='coerce')
df['prod_period_to'] = pd.to_datetime(df['prod_period_to'], errors='coerce')
df['recall_start'] = pd.to_datetime(df['recall_start'], errors='coerce')

# MySQL에 저장 (✨ 여기서는 "origin_data"라는 테이블에 넣는다고 가정할게)
df.to_sql(name='origin_data', con=db, if_exists='append', index=False)

print("✅ CSV 원본 데이터 MySQL에 저장 완료")

