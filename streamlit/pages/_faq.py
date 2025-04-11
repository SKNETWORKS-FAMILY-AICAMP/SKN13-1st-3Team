import streamlit as st
import pandas as pd
import pymysql
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
import time
import random

# Create 3 columns: left, center, right
col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([3, 5, 3, 5, 3, 5, 3, 5, 3])  # Adjust ratio if needed

with col6:
    st.page_link("pages/_faq.py", label="FAQ")

with col8: 
    st.page_link("pages/_download.py", label = "Downloads")

with col4:
    st.page_link("pages/_graphs.py", label="Oil Price")

with col2:
    st.page_link("pages/home.py", label="Home")

st.write("                                ")
st.write("                                ")
st.subheader("FAQ")
st.write("아래는 자주 물어보는 질문들입니다.")

# CSV 파일 경로 설정
# csv_path = "../crawling/주유소정보.csv"  # 경로는 상황에 맞게 조정하세요

# # 데이터 불러오기
# df = pd.read_csv(csv_path)

# conn = pymysql.connect(
#         host='192.168.0.45', # DB 주소 (예: '127.0.0.1' 또는 AWS RDS 주소)
#         port = 3306,
#         user='3team',    # MySQL 사용자
#         password='1111',
#         db='gas_station',
#         charset='utf8'  # 저장할 데이터베이스명
#     )

import pandas as pd

# SQL 쿼리 실행하여 데이터 가져오기
# query = """
#     SELECT gs.*, b.brand_name 
#     FROM gas_station gs
#     JOIN brand b ON gs.brand_id = b.brand_id
# """
# df = pd.read_sql(query, conn)

# # 연결 종료
# conn.close()

#print(df.head())


#faq
    
faq_list = [
    {
        "Q": "서울시 외 도시들은 제공하지 않나요?",
        "A": "현재는 서울시만 제공하고 있습니다."
    },
    {
        "Q": "모바일에서 사용 가능한가요?",
        "A": "현재는 PC 화면에 최적화되어 있으며, 모바일 최적화는 준비 중입니다."
    },
    {
        "Q": "게시되는 유가는 세금을 포함하고 있나요?",
        "A": "모든 유가는 부가가치세 등 모든 세금이 포함된 최종 가격입니다."
    },
    {
        "Q": "주유소 가격 리스트를 다운로드하고 싶어요",
        "A": "Home > Downloads 에서 .csv 형식으로 다운로드할 수 있습니다"
    },
    {
        "Q": "근처 주유소를 알고 싶어요",
        "A": "OpenOil 홈페이지에서 원하는 구로 필터를 하여 정보를 얻을 수 있습니다."
    },
    {
        "Q": "24시간 주유소를 알고 싶어요",
        "A": "부가 옵션에서 해당 옵션 체크박스 선택시 적용되어 표시됩니다."
    },
    {  
        "Q": "주유소 브랜드별 카드 혜택이 알고 싶어요.",
        "A":"각 사이트에서 참고하세요." 
            """
        <div style="display: flex; gap: 100px; margin: 10px 0; justify-content: center;">
            <a href="https://www.enclean.com/benefit/card" target="_blank" style="text-decoration: none;">
                <div style="display: flex; align-items: center; gap: 8px; margin: 10px 0;">
                    <img src="//i.namu.wiki/i/riYiv3lUtT_OPEI9peqE1tazyyFKAmMlQXL_IEWbbOuFF7CQ60nMDrVGVBmn8HOMDy3YoFajNFfMDRytF2DtblJdzCIfMWpUbEIYqfogfA1UsaqgboPZX-2AKUIIiXqQTvoMabI53Iscat6tIUPZ9Q.svg" width="100"/>
                </div>
            </a>
            <a href="https://gscenergyplus.com/creditcard/introduction" target="_blank" style="text-decoration: none;">
                <div style="display: flex; align-items: center; gap: 8px; margin: 10px 0;">
                    <img src="https://i.namu.wiki/i/eN-uazuirDtPwLDTvuY1tC_NqySz575ZObpMMcH6tBw93LgAh4rLoMcTmVXXBd0eoWii9sUnMRhwXF9QgF8RwB7RBKkm0cJa_pKWd9e_YlQJ_Ltm-8JSDQVWLh01mgX0KfFDf_30rAOEjfXzdH63Sw.svg" width="200"/>
                </div>
            </a>
            <a href="https://www.s-oilbonus.com/bcard/A-Bcard-Guide-001" target="_blank" style="text-decoration: none;">
                <div style="display: flex; align-items: center; gap: 8px; margin: 20px 0;">
                    <img src="https://i.namu.wiki/i/jlWT03ohLke01SpBNxOum98tFtgUCeSzn_RHSZCErFl1ymAK6RsHjCCkXFnxN1hy3luNc-fTk177zkE6Thr8N30DJyaUnlk5Rs5EL1TSxZOklY2ckC_Fg6bCWx5o8di60KOlCu6gJpgSn4b-m4aqOg.svg" width="200"/>
                </div>
            </a>
            <a href="https://www.s-oilbonus.com/bcard/A-Bcard-Guide-001" target="_blank" style="text-decoration: none;">
                <div style="display: flex; align-items: center; gap: 8px; margin: 10px 0;">
                    <img src="https://i.namu.wiki/i/bR6ttb3OIMHf1OIWVWmu_rNsm02Habx-brRkPGc-opNhzFmIyK1XtJA5x3jOWiJltumpx9sd7CNHyUgLqnsBvDjvTfAoo5taeG2ETuTzV-lu4N9CxSpnScNUrmDpN6csyrcR0eB2H4s6pVGBrw639A.svg" width = "100"/>
                </div>
            </a>
        </div>
        """
    },
    {
        "Q": "알뜰주유소란 무엇인가요",
        "A": (
            "대한민국 정부가 추진하는 주유소 사업입니다. 원래 목적은 대형 정유사의 독과점 상황인 "
            "석유 제품의 소매 유통 방식을 개선하여 더욱 저렴한 가격에 기름을 공급하겠다는 것이었으며, "
            "현재는 한국석유공사의 자영 알뜰 주유소, 한국도로공사의 고속도로 주유소(ex-OIL), "
            "농업협동조합의 농협 주유소(NH-OIL)라는 세 가지 형태로 전국에 약 1,180 곳이 영업 중입니다."
        )
    },
    {
        "Q": "공장도 가격과 오피넷에 공개되고 있는 정유사 또는 대리점 가격의 차이가 궁금합니다",
        "A": ("1997년 유가자유화가 실시된 후에 석유제품의 가격은 정유사, 대리점, 주유소 등 석유 제품 각 단계별 판매자가"
              "자율적으로 결정하고 있습니다. 그리고 흔히 정유사나 대리점에서 이야기하는 공장도 가격은 공식적인 가격이 아닙니다."
              "실제로 정유사 등이 공급할 때의 가격은 유통비용이나 판매 대상에 따라 달라질 수 있습니다. 반면에 OpenOil에서 공개하고"
              " 있는 정유사 공급(판매)가격은 정유사 등이 주유소, 대리점, 판매처에 판매한 내수매출액을 내수 판매량으로 나눈 제품별 "
              "물량 가중 평균 판매가격을 말합니다. 이는 석유 및 석유대체연료 사업법 제38조의2에 근거하여 석유판매업자들에게 가격보고를" 
              "받고 이를 공개하는 것으로 실제적으로 정유사나 대리점에서 공급하는 가격과는 차이가 있을 수 있습니다. 감사합니다.")
    },
    {
        "Q": "정유사 공급가격과 판매가격의 차이가 무엇인가요?",
        "A": ("정유사 공급가격은 정유사가 직영을 제외한 대리점, 주유소 및 판매처에 판매한 물량 및 금액을 가지고 산정한 가격으로 "
              "매주 자료가 나옵니다. 반면 정유사 판매가격은 직영을 포함한 모든 거래처에 판매한 물량에 대한 가격으로 매달 자료가 "
              "나오며 이달의 수치는 다음달 말 경에 나오게 됩니다.")
    }
]

# FAQ 출력
for faq in faq_list:
    with st.expander(faq["Q"]):
        st.markdown(faq["A"], unsafe_allow_html=True)  # 줄바꿈 및 마크다운 적용


st.page_link("app.py", label="Go Home")