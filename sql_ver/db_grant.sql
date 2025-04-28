-- mysql을 설치했다면, Window Service(백그라운드 프로세스)에서 확인할 수 있다.

show databases; -- = show schemas; / 서버에 존재하는 모든 데이터베이스(스키마) 목록을 보여줌
#use mysql; -- mysql 데이터베이스(시스템 DB)를 사용하겠다고 지정
use SKN14_1st_6Team; -- mysql 데이터베이스(시스템 DB)를 사용하겠다고 지정

# DROP DATABASE skn14_1st_6Team;

# 새로운 계정 user 생성 (root 관리자 계정만 가능)
# - user
# - host: %는 모든 ip를 의미 (아무데서나 접근 가능)
# - identified by 비밀번호 (대소문자 구분)
create user 'skn14'@'%' identified by 'skn14';

# (root 관리자계정) 새로운 database(schema) 생성
create database SKN14_1st_6Team;

# skn14계정이 SKN14_1st_6Team를 사용
grant all privileges on SKN14_1st_6Team.* to 'skn14'@'%';

show grants for 'skn14'@'%';