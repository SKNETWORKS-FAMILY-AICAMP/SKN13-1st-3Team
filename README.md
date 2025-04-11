# SKN13-1st-3Team

## 1. 📌 프로젝트 개요
프로젝트명: 서울시 주유소 현황 및 관련 정보 제공 시스템
목표: 서울시 내 주유소의 위치, 유가, 브랜드, 운영 시간 등의 정보를 웹에서 자동으로 수집하고, 사용자에게 쉽게 제공하는 시스템을 개발한다.

## 프로젝트 소개

-  석유공사가 운영하는 유가정보 서비스를 바탕으로 서울시 내의 400여개 주유소의 실시간 판매가격 및 부가시설 정보를 제공
- 위치정보 기반으로 상세위치 정보 제공 및 고객센터 정보 제공
- 주유소 및 제공서비스 관련 FAQ 조회 시스템 제공

### 주제 선정 이유(필요성)
- 변동성이 많은 유가로 유가 상승시에 '소비자' 부담이 커짐
- 기름값은 지역별, 주유소별로 차이가 있기 때문에 어디서 주유하느냐에 따라서 비용을 절약할 수도 낭비할 수도 있음
-  각 지역별, 주유소별 가격 비교 및 위치 정보 제공 고객센터 대표번호 및 부가 시설에 따른 정보를 한번에 확인 가능하다면 현명한 소비가 가능 할 것이라고 생각하여 제작.

<![Image](https://github.com/user-attachments/assets/75f6e738-dabe-4c60-98e1-52441828a64f)\><![Image](https://github.com/user-attachments/assets/65a116cf-5ec6-4680-8a08-4c39fd7c400d)\>

## 2. 🎯 주요 기능
### 2.1 데이터 크롤링 기능
 서울시 주유소 정보를 제공하는 웹사이트(예: 오피넷, 서울시 열린데이터광장 등)에서 실시간 데이터 수집

크롤링 항목:

- 주유소 이름
- 주소
- 브랜드(SK, GS, S-OIL 등)
- 유가(휘발유, 경유 등)
- 셀프 여부
- 운영 시간(24시간 여부 등)
- 편의 시설(화장실 등등)

크롤링 주기 설정 가능 (예: 하루 1회 자동 갱신)

 중복 및 오류 데이터 제거

### 2.2 데이터 저장 및 관리

수집된 데이터를 CSV, JSON 혹은 DB에 저장

### 2.3 검색 기능

- Streamlit UI 상에서 서울 지도에 주유소 위치 마커 표시
- 유가 기준 정렬 기능 (예: 휘발유 가격 낮은 순)
- 브랜드/구별 필터링 기능
- 특정 구의 평균 유가 시각화 (막대그래프 등)

### 2.4 UI (Streamlit 기반)

- 사용자 검색창 제공 (구 이름, 주유소 이름 등)
- 지도 시각화 기능
- 최신 데이터 확인 및 다운로드 기능

 
## 3. 🔧 기술 스택
- 항목	기술
- 언어	Python
- 웹 크롤링	BeautifulSoup, Selenium
- 데이터 저장	Pandas, CSV, mysql
- 시각화	Streamlit, Plotly, pydeck
- 배포	Streamlit Cloud 또는 로컬 실행



## 4.1 기능적 요구사항(Functional Requirements)
|ID|요구사항 설명|
|------|---|
|FR-01	|사용자에게 주유소 정보를 시각화하여 지도에 표시해야 한다.|
|FR-02	|사용자는 지역(구), 브랜드, 가격 범위 등을 기준으로 필터링할 수 있어야 한다.|
|FR-03	|사용자는 주유소 이름, 주소, 브랜드로 검색할 수 있어야 한다.|
|FR-04	|사용자는 필터링된 주유소 목록을 CSV 파일로 다운로드할 수 있어야 한다.|
|FR-05	|지역별 평균 휘발유 및 경유 가격을 바차트로 시각화해야 한다.|
|FR-06  |날짜별 평균 휘발유 및 경유 가격을 꺾은선 그래프 시각화해야 한다.|
|FR-07  |FAQ 페이지를 통해 자주 묻는 질문에 대한 답변을 제공해야 한다.|
|FR-08	|페이지 간 이동은 네비게이션 바 및 '홈으로 가기' 버튼으로 구현되어야 한다.|
|FR-09	|지도 위 주유소 마커는 브랜드별로 구분된 색상으로 표시되어야 한다.|

## 4.2 비기능적 요구사항(Non-Functional Requirements)
|ID|요구사항 설명|
|------|---|
|NFR-01|대시보드는 초기 로딩 시 3초 이내에 화면을 출력해야 한다|
|NFR-02|필터 적용시 로딩이 5초 이내에 되어야 한다|
|NFR-03|데이터는 MySQL 서버에서 실시간으로 불러와야 하며, 업데이트 주기는 1일이다.|
|NFR-04|대시보드는 PC 환경에 최적화되어야 한다|




## 4. FAQ

1. Q. 서울 외 지역 주유소 정보는 제공하나요? A. 현재는 서울 지역만 지원하고 있으며, 다른 지역은 추후 업데이트될 예정입니다. 
2. lpg, 고급휘발유 가격 정보
3. 유가 가격 초기화 시간
4. 유가 세금 포함 여부
5. 모바일에서 사용 가능한가요? A. 현재는 PC 화면에 최적화되어 있으며, 모바일 최적화는 준비 중입니다.\
6. 알뜰주유소란 무엇인가요 

주유소 정보 사이트 url 연결(soil, sk, gs 등등)


## 5. 📅 일정 계획 (예시)
	1. 대상 사이트 조사 및 크롤링 구조 설계
	2. 크롤러 개발 및 데이터 저장 기능 구현
	3. 데이터 시각화 기능 개발
	4. UI 개발 및 기능 통합
	5. 테스트, 문서화

## 6. ✅ 기대 효과
서울시 주유소 유가 정보 실시간 확인 가능

사용자 맞춤형 주유소 추천 가능

## 7. 사용한 기술 스택

|종류|TOOL명
|-----|---|
|언어| <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">|
|웹크롤링|<img src="https://img.shields.io/badge/selenium-4479A1?style=for-the-badge&logo=selenium&logoColor=white">|
|데이터저장|<img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white">|
|데이터 시각화|<img src="https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white">|
|화면구현|<img src="https://img.shields.io/badge/streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white">,<img src="https://img.shields.io/badge/html-E34F26?style=for-the-badge&logo=html&logoColor=white">,<img src="https://img.shields.io/badge/css-663399?style=for-the-badge&logo=css&logoColor=white">|
