# SKN14-1st-6Team

---
- SK 네트웍스 AI Camp 1차 프로젝트


## 팀명

---
### 아비터 리콜(Arbiter Recall)
   사용자와 차량 간의 중재자(Arbiter)가 되어 리콜 정보를 더 상세하게 제공하여 사용자가 더 쉽게 구매할 차량을 선택할 수 있도록 합니다.
   <br>
   <br>

## 팀원소개

---
 <table>
  <tr>
    <td align="center">
    서
7. 수행 결과
8. 팀원 별 회고

## 1. 프로젝트 개요

---
### 1.1 주제
자동차는 현대인의 생활 필수품이 되었지만, 그에 따른 품질 문제나 안전상의 결함 이슈가 꾸준히 발생
특히 리콜(Recall)은 제조사의 자발적 조치이거나 정부기관의 강제 명령에 의해 이루어지는데, 
리콜 이력이 있는 차량은 안전성에 영향을 줄 수 있고, 향후 중고차 거래 시 감가 요인이 되기도 합니다.
본 프로젝트는 차량 구매자 또는 차량 소유자들이 자신이 관심 있는 자동차 모델의 리콜 이력을 쉽게 조회하고, 
이를 다양한 조건(제조사, 모델명, 생산기간, 리콜사유 등)으로 필터링할 수 있도록 지원하는 시스템을 개발하는 것을 목표로 함
Streamlit을 사용하여 웹 기반 대시보드 형태로 구현하고, Python으로 데이터 수집 및 처리, 
MySQL로 데이터베이스를 관리하여 효율적이고 직관적인 사용자 경험을 제공하고자 합니다.

### 1.2 필요성
신뢰할 수 있는 차량 구매를 돕기 위한 데이터 기반 시스템의 필요성

1. 자동차 안전이슈에 대한 관심 증가
최근 몇 년간 대규모 리콜 사례(에어백, 브레이크 결함 등)가 사회적 문제로 떠오르면서, 소비자들은 차량 안전성에 대한 관심이 높아졌습니다. 
하지만 개별 차량의 리콜 여부를 직접 조사하는 것은 매우 번거롭고 정보 접근성이 낮습니다. 따라서 이를 누구나 쉽게 조회할 수 있는 서비스가 필요합니다.
2. 정부 데이터 개방과 활용 촉진
국내외 정부 기관은 차량 리콜 데이터를 공개하고 있지만, 일반 사용자가 직접 활용하기에는 검색 기능이 제한적이거나 UI가 불편합니다. 
이를 보다 친숙하고 가벼운 인터페이스로 가공해 제공하면, 공공 데이터 활용도를 높이는 데에도 기여할 수 있습니다.


### 1.3 관련 뉴스 기사 (참고 자료)
- **국내 차량** (https://www.chungnamilbo.co.kr/news/articleView.html?idxno=814343)
<img src="https://github.com/skn-ai14-250409/SKN14-1st-6Team/blob/main/Docs/imgs/readmenews_01.png?raw=true" width=500>

- **수입 차량** (https://biz.heraldcorp.com/article/10461563?ref=naver)
<img src="https://github.com/skn-ai14-250409/SKN14-1st-6Team/blob/main/Docs/imgs/readmenews_02.png?raw=true" width=500>

### 1.4 목표
자동차 리콜 이력 조회를 통해 차량 구매자와 소유자가 보다 신뢰성 있는 결정을 내릴 수 있도록 지원하는 시스템 개발
이번 프로젝트의 최종 목표는 차량 리콜 이력을 쉽고 직관적으로 조회할 수 있는 데이터 기반 플랫폼을 구축하는 것입니다.
특히 다양한 조건(제조사, 차종, 생산기간, 전기차 여부, 국산/수입 여부 등)에 따라 데이터를 필터링하고,
시각적으로 리콜 이력을 한눈에 확인할 수 있도록 하여 사용자 편의성을 극대화하는 것을 지향합니다.
이를 통해 다음과 같은 구체적인 목표를 달성하고자 합니다.
1. 사용자 친화적인 리콜 조회 시스템 구현
Streamlit 기반의 간편하고 직관적인 UI를 설계하여, IT 지식이 없는 사용자도 쉽게 리콜 정보를 조회할 수 있도록 합니다.
제조사, 차종, 생산기간, 리콜사유 등 다양한 필터 기능을 제공하여 맞춤형 검색을 지원합니다.
2. 신뢰성 있는 데이터 수집 및 관리
정부 기관 및 신뢰할 수 있는 공개 데이터를 기반으로, 웹 크롤링 및 수집 자동화 시스템을 구축합니다.
수집된 데이터를 정제하여 MySQL 데이터베이스에 체계적으로 저장하고, 효율적인 조회를 위해 최적화된 ERD를 설계합니다.
3. 데이터 기반 차량 비교 및 의사결정 지원
사용자가 특정 제조사나 모델을 선택했을 때, 해당 차량의 리콜 이력과 주요 문제점을 시각화하여 제공합니다.
구매 결정에 참고할 수 있도록, 리콜 사유별 분포도, 리콜 건수, 생산기간 등 다양한 통계 정보를 함께 제시합니다.
4. 팀원 기술 역량 강화 및 실전 프로젝트 경험 축적
Python, SQL, Streamlit을 활용한 데이터 파이프라인을 직접 구축하고, 프론트-백엔드 전체 과정을 경험함으로써 실전 개발 역량을 키웁니다.
프로젝트 협업 과정을 통해 문제 해결 능력, 커뮤니케이션 능력, 데이터 처리 및 분석 능력을 향상시킵니다.

## 2. 프로젝트 구성

---
### 2.1 주요 기술 스택
| 분류 | 기술                                                                                                                                                                                                                                                                                                            |
|:---|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 언어 | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white)                                                                                                                                                                                                         |
| 웹크롤링 | ![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=Selenium&logoColor=white)                                                                                                                                                                                                   |
| 데이터저장 | ![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=MySQL&logoColor=white)                                                                                                                                                                                                            |
| 데이터 시각화 | ![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=Pandas&logoColor=white) ![Matplotlib](https://img.shields.io/badge/Matplotlib-3776AB?style=for-the-badge)                                                                                                                       |
| 화면구현 | ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white) ![HTML](https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=HTML5&logoColor=white) ![CSS](https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=CSS3&logoColor=white) |

### 2.2 프로젝트 구조


### 2.3 기능적 요구 사항
- 사용자 입력을 통한 차량 검색
- 검색한 차량의 리콜 이력 확인 및 필터링
- 리콜 상세 정보 제공 및 시각화

### 2.4 Front-end
1) Streamlit 기반의 간편한 UI
2) 데이터 실시간 필터링 기능 지원
3) 직관적인 시각화 기능 지원


### 2.5 Back-end
1) MySQL을 통한 데이터 관리
2) 크롤링을 통한 데이터 수집 자동화
3) ERD 설계


## 3. 주요 기능 설명

---
### 3.1 데이터 수집 및 관리
- 데이터셋 수집 -> 데이터 전처리 -> MySQL 저장
- 매년 데이터 갱신

### 3.2 데이터 조회 및 필터링
- 제조사, 차종, 전기차 여부, 생산기간 등 다양한 조건 검색
- 데이터 조회 시 관련 정보 제공

### 3.3 데이터 시각화
- 리콜 사유 분포 차트
- 상세 리콜 내역 테이블 
- 리콜 이력 지도 시각화 

## 4. 서비스 화면 구성

---
### 4.1 메인 페이지
- 배너 1
- 배너 2
- 배너 3


### 4.2 세부 페이지_1
- 배너 1
- 배너 2
- 배너 3

### 4.2 세부 페이지_2
- 배너 1
- 배너 2
- 배너 3


## 5. ERD (Entity Relationship Diagram)
<img src="https://github.com/skn-ai14-250409/SKN14-1st-6Team/blob/main/Docs/physic_ERD.png?raw=true" width=500>

### 6. 테이블 기술서
<img src="https://github.com/skn-ai14-250409/SKN14-1st-6Team/blob/main/Docs/table_skill_west.png?raw=true" width=500>

*docs 문서 참조*

### 7. 프로젝트 시연


### 8. 프로젝트 회고록



