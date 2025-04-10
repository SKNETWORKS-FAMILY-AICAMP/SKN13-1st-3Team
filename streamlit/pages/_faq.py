import streamlit as st
import pandas as pd
import pymysql
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
import time
import random

st.title("FAQ")
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
        "A": "현재는 서울시만 제공합니다."
    },
    {
        "Q": "주유소 가격 리스트를 다운로드하고 싶어요",
        "A": "메인 화면에 'CSV 다운로드' 버튼이 있습니다. 해당 버튼을 누르면 서울 주유소 판매가격 리스트를 .csv 파일로 다운로드 받으실 수 있습니다."
    },
    {
        "Q": "모바일에서 사용 가능한가요?",
        "A": "현재는 PC 화면에 최적화되어 있으며, 모바일 최적화는 준비 중입니다."
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
        "Q": "유가 세금 포함 여부",
        "A": "X"
    },
    {
        "Q": "유가 가격 초기화 시간",
        "A": "매일"
    },
    {
        "Q": "LPG, 고급휘발유 가격 정보는 어디서 얻을 수 있나요?",
        "A": "오피넷 홈페이지([https://www.opinet.co.kr/searRgSelect.do]) 에서 확인 가능합니다."
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
    }
]


# FAQ 출력
for faq in faq_list:
    with st.expander(faq["Q"]):
        st.markdown(faq["A"], unsafe_allow_html=True)  # 줄바꿈 및 마크다운 적용


st.page_link("app.py", label="Go Back")

