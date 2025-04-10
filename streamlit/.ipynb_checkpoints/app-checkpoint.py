import streamlit as st
import pandas as pd

st.set_page_config(page_title="서울시 주유소 대시보드", layout="wide")
st.title("서울시 주유소 정보 대시보드")

# CSV 파일 경로 설정
# csv_path = "../crawling/주유소정보.csv"  # 경로는 상황에 맞게 조정하세요

# # 데이터 불러오기
# df = pd.read_csv(csv_path)

import pymysql

conn = pymysql.connect(
        host='192.168.0.45', # DB 주소 (예: '127.0.0.1' 또는 AWS RDS 주소)
        port = 3306,
        user='3team',    # MySQL 사용자
        password='1111',
        db='gas_station',
        charset='utf8'  # 저장할 데이터베이스명
    )

import pandas as pd

# SQL 쿼리 실행하여 데이터 가져오기
query = "SELECT * FROM gas_station"  # 테이블 이름이 'gas_stations'라고 가정
df = pd.read_sql(query, conn)

# 연결 종료
conn.close()

print(df.head())

# 데이터 확인
# print(df.head())  # 처음 5개 행 출력
# print(df.info())  # 데이터프레임 정보 출력

# 휘발유, 경유 → 숫자형으로 변환 (쉼표 제거 및 에러 무시)
df["gasoline_price"] = pd.to_numeric(df["gasoline_price"].astype(str).str.replace(",", "").str.strip(), errors="coerce")
df["diesel_price"] = pd.to_numeric(df["diesel_price"].astype(str).str.replace(",", "").str.strip(), errors="coerce")

# 필터 옵션
gu_options = ["전체"] + sorted(df["region"].dropna().unique().tolist())
brand_options = sorted(df["brand_name"].dropna().unique())

st.sidebar.header("🔍 필터 옵션")
selected_gu = st.sidebar.selectbox("지역 선택", gu_options)
selected_brand = st.sidebar.multiselect("브랜드 필터", brand_options, default=brand_options)
sort_option = st.sidebar.radio("가격 정렬", ["휘발유 높은순", "휘발유 낮은순"])
price = st.sidebar.slider ('가격' , 0 , 3000, step=10, format="%d원")
# 필터 적용
filtered = df.copy()

if selected_gu != "전체":
    filtered = filtered[filtered["region"] == selected_gu]

filtered = filtered[filtered["brand_name"].isin(selected_brand)]

if sort_option == "휘발유 높은순":
    filtered = filtered.sort_values("gasoline_price", ascending=True)
else:
    filtered = filtered.sort_values("gasoline_price", ascending=False)

# 검색 기능 추가
search_term = st.text_input("🔍 주유소 검색", placeholder="주유소 이름, 주소, 브랜드로 검색")

if search_term:
    # 대소문자 구분 없이 검색
    search_filter = (
        filtered["station_name"].str.contains(search_term, case=False, na=False) |
        filtered["address"].str.contains(search_term, case=False, na=False) |
        filtered["brand_name"].str.contains(search_term, case=False, na=False)
    )
    filtered = filtered[search_filter]

# 필터된 데이터 테이블 출력
st.subheader(f"📋 {selected_gu}의 주유소 목록")
st.dataframe(filtered.reset_index(drop=True), use_container_width=True, hide_index = True)

# 평균 가격 시각화
st.subheader("📊 구별 평균 가격")

# 휘발유와 경유를 별도의 차트로 표시
col1, col2 = st.columns(2)

with col1:
    st.subheader("휘발유 평균 가격")
    mean_gasoline = df.groupby("region")["gasoline_price"].mean().round(1)
    st.bar_chart(mean_gasoline)

with col2:
    st.subheader("경유 평균 가격")
    mean_diesel = df.groupby("region")["diesel_price"].mean().round(1)
    st.bar_chart(mean_diesel)

#faq
st.subheader("FAQ-자주 묻는 질문")
faq_list = [
    {
        "Q": "서울시 외 도시들은 제공하지 않나요?",
        "A" : "현재는 서울시만 제공합니다."
    },
    {
        "Q": "모바일에서 사용 가능한가요?",
        "A" : "현재는 PC 화면에 최적화되어 있으며, 모바일 최적화는 준비 중입니다"
    },
    {
        "Q": "알뜰주유소란 무엇인가요",
        "A" : "대한민국 정부가 추진하는 주유소 사업이다. 원래 목적은 대형 정유사의 독과점 상황인 석유 제품의 소매 유통 방식을 개선하여 더욱 저렴한 가격에 기름을 공급하겠다는 것이었으나, 현재 한국석유공사의 자영 알뜰 주유소, 한국도로공사의 고속도로 주유소(ex-OIL), 농업협동조합의 농협 주유소(NH-OIL)라는 세 가지 형태로 전국에 약 1,180 곳이 영업중이다."
    },
    {
      "Q": "LPG, 고급휘발유 가격 정보는 어디서 얻을 수 있나요?",
        "A" : "오피넷 홈페이지(https://www.opinet.co.kr/searRgSelect.do) 에서 얻을 수 있습니다."
    },
    {
      "Q": "주유소 브랜드별 카드 혜택이 알고 싶어요.",
        "A" : "**[SK주유소](https://www.enclean.com/benefit/card)**"
              "**[GS주유소](https://gscenergyplus.com/creditcard/introduction)**"
              "**[현대오일뱅크](http://www.oilbankcard.com/m2012/front/creditNew.do)**"
              "**[S-OIL](https://www.s-oilbonus.com/bcard/A-Bcard-Guide-001)"
    }
]

for faq in faq_list:
    with st.expander (faq["Q"]):
        st.write(faq["A"])

##유가 가격 초기화 시간
##유가 세금 포함 여부







# CSV 다운로드
st.download_button(
    label="CSV 다운로드",
    data=filtered.to_csv(index=False, encoding="utf-8-sig"),
    file_name=f"{selected_gu}_주유소정보.csv",
    mime="text/csv"
)
