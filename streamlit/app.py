import streamlit as st
import pandas as pd
import pymysql
import altair as alt
import folium
import os
import time
import random

from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
from streamlit_navigation_bar import st_navbar

st.set_page_config(page_title="서울시 주유소 대시보드", layout="wide")

# Create 3 columns: left, center, right
col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([3, 5, 3, 5, 3, 5, 3, 5, 3])  # Adjust ratio if needed

with col6:
    st.page_link("pages/_faq.py", label="FAQ")

with col8: 
    st.page_link("pages/_download.py", label = "Downloads")

with col4:
    st.page_link("pages/_graphs.py", label="Oil Price")

with col2:
    st.page_link("pages/_aa.py", label="Home")


# # Define the pages for the navigation bar
# pages = ["Home", "Documentation", "Examples", "Community", "About"]
# # Create the navigation bar
# page = st_navbar(pages)
# # Display the selected page
# st.write(page)

# CSS 스타일 적용
st.markdown("""
    <style>
    /* GS칼텍스 */
    span[aria-label="GS칼텍스, close by backspace"] {
        background-color: #FFA500 !important;  /* 초록색 */
        color: white !important;
    }
    
    /* HD현대오일뱅크 */
    span[aria-label="HD현대오일뱅크, close by backspace"] {
        background-color: #79B3EA !important;  /* 파란색 */
        color: white !important;
    }
    
    /* S-OIL */
    span[aria-label="S-OIL, close by backspace"] {
        background-color: #48B445 !important;  /* 초록색 */
        color: white !important;
    }
    
    /* SK에너지 */
    span[aria-label="SK에너지, close by backspace"] {
        background-color: #FF0000 !important;  /* 빨간색 */
        color: white !important;
    }
    
    /* 알뜰주유소 */
    span[aria-label="알뜰주유소, close by backspace"] {
        background-color: #9F468F !important;  /* 보라색 */
        color: white !important;
    }
    
    /* 정호주유소 */
    span[aria-label="정호주유소, close by backspace"] {
        background-color: #808080 !important;  /* 회색 */
        color: white !important;
    }
    
    /* 호버 효과 */
    span[aria-label*="close by backspace"]:hover {
        opacity: 0.8 !important;
    }
    </style>
""", unsafe_allow_html=True)

# CSV 파일 경로 설정
csv_path = "../crawling/2025-04-10.csv"  # 경로는 상황에 맞게 조정하세요

# # 데이터 불러오기
df = pd.read_csv(csv_path)

conn = pymysql.connect(
        host='192.168.0.45', # DB 주소 (예: '127.0.0.1' 또는 AWS RDS 주소)
        port = 3306,
        user='3team',    # MySQL 사용자
        password='1111',
        db='gas_station',
        charset='utf8'  # 저장할 데이터베이스명
    )

# SQL 쿼리 실행하여 데이터 가져오기
query = """
    SELECT gs.*, b.*
    FROM gas_station gs
    JOIN brand b ON gs.brand_id = b.brand_id
"""
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

st.sidebar.image("openoil.png", width=800)
# st.sidebar.header("🔍 필터 옵션")
selected_gu = st.sidebar.selectbox("지역 선택", gu_options)
selected_brand = st.sidebar.multiselect("브랜드 필터", brand_options, default=brand_options)

# # st.write(page)
# st.write("부가 옵션")
# col1, col2, col3, col4 = st.columns(4)

# with col1:
#     self_service = st.checkbox("셀프 주유소")
# with col2:
#     car_wash = st.checkbox("세차장")
# with col3:
#     convenience_store = st.checkbox("편의점")
# with col4:
#     open_24h = st.checkbox("24시 운영")

#체크박스 필터링 된 데이터 출력
# 사이드바 체크박스
st.sidebar.write("부가 옵션")
self_service = st.sidebar.checkbox("셀프 주유소", key="self_checkbox")
car_wash = st.sidebar.checkbox("세차장", key="wash_checkbox")
convenience_store = st.sidebar.checkbox("편의점", key="store_checkbox")
open_24h = st.sidebar.checkbox("24시 운영", key="24h_checkbox")
 
# 필터링 준비

filtered = df.copy()

# NaN 제거 (없으면 필터링 실패함)
filtered = filtered.fillna({
    "self_service": "N",
    "car_wash": "N",
    "convenience_store": "N",
    "hours_24": "N"
})

# 각 체크박스의 상태에 따라 필터링
if self_service:
     filtered = filtered[filtered["self_service"]=="Y"]
if car_wash:
     filtered = filtered[filtered["car_wash"]=="Y"]
if convenience_store:
     filtered = filtered[filtered["convenience_store"]=="Y"]
if open_24h:
     filtered = filtered[filtered["hours_24"]=="Y"]
    
# 사이드바 가격정렬
sort_option = st.sidebar.radio("가격 정렬", ["휘발유 낮은순", "경유 낮은순"])
# 사이드바 가격슬라이더
price_gasoline = st.sidebar.slider ("휘발유 가격" , 0 , 3000, step=10, format="%d원", key="price_gasoline_slider", value = 3000)
price_diesel = st.sidebar.slider ("경유 가격" , 0 , 3000, step=10, format="%d원", key="price_diesel_slider", value = 3000)

  
# 필터 적용

if selected_gu != "전체":
    filtered = filtered[filtered["region"] == selected_gu]

filtered = filtered[filtered["brand_name"].isin(selected_brand)]

if sort_option == "휘발유 낮은순":
    filtered = filtered.sort_values("gasoline_price", ascending=True)
if sort_option == "경유 낮은순":
    filtered = filtered.sort_values("diesel_price", ascending=True)
filtered = filtered[filtered["gasoline_price"] <= price_gasoline]
filtered = filtered[filtered["diesel_price"] <= price_diesel]

# 검색 기능 추가
st.markdown("### 주유소 검색")
search_term = st.text_input("", placeholder="주유소 이름, 주소, 브랜드로 검색", label_visibility="collapsed")

if search_term:
    # 대소문자 구분 없이 검색
    search_filter = (
        filtered["station_name"].str.contains(search_term, case=False, na=False) |
        filtered["address"].str.contains(search_term, case=False, na=False) |
        filtered["brand_name"].str.contains(search_term, case=False, na=False)
    )
    filtered = filtered[search_filter]

# 브랜드별 색상 매핑 함수
def get_brand_color(brand):
    # 브랜드별 고정 색상 매핑
    brand_colors = {
        'GS칼텍스': 'orange',
        'S-OIL': 'green',
        'SK에너지': 'red',
        'HD현대오일뱅크': 'blue',
        '알뜰주유소': 'purple',
        '코끼리주유소': 'gray',
        '정호주유소': 'gray',
    }
    return brand_colors.get(brand, 'gray')  # 기본값은 회색

# 지도 표시 함수
def show_map(filtered_data):
    # 서울 중심 좌표
    m = folium.Map(
        location=[37.5665, 126.9780], 
        zoom_start=11
    )
    
    # 각 주유소에 대해 마커 추가
    for idx, row in filtered_data.iterrows():
        if pd.notnull(row['latitude']) and pd.notnull(row['longitude']):
            # HTML을 사용하여 팝업 텍스트 포맷팅
            popup_text = f"""
            <div style='font-family: Arial; font-size: 14px;'>
                <b>{row['station_name']}</b><br>
                <span style='color: #666;'>{row['brand_name']}</span><br>
                <span style='color: #666;'>TEL. {row['cst_service']}</span>
                <div style='margin-top: 5px;'>
                    <span style='color: #e74c3c;'>휘발유: {row['gasoline_price']}원</span><br>
                    <span style='color: #3498db;'>경유: {row['diesel_price']}원</span>
                </div>
            </div>
            """
            popup = folium.Popup(popup_text, max_width=300)
            
            folium.Marker(
                [row['latitude'], row['longitude']],
                popup=popup,
                tooltip=row['station_name'],
                icon=folium.Icon(color=get_brand_color(row['brand_name']))
            ).add_to(m)
    
    return m

# 지도 표시
map = show_map(filtered)
folium_static(map, width=None, height=600)

# 필터된 데이터 테이블 출력

columns_to_show = ["station_name", "address", "brand_name", "gasoline_price", "diesel_price"]
filtered_display = filtered[columns_to_show]
filtered_display = filtered_display.rename(columns={
    "station_name": "주유소 이름",
    "address": "주소",
    "brand_name": "브랜드",
    "gasoline_price": "휘발유 가격",
    "diesel_price": "경유 가격"
})
# st.subheader(f"📋 {selected_gu}의 주유소 목록")
st.dataframe(filtered_display.reset_index(drop=True), use_container_width=True, hide_index=True)

# # 평균 가격 시각화
# st.subheader("📊 구별 평균 가격")

# # 평균 가격 계산
# mean_prices = df.groupby("region")[["gasoline_price", "diesel_price"]].mean().round(1).reset_index()

# # 긴 형식으로 변환
# mean_prices_melted = mean_prices.melt(id_vars="region", 
#                                       value_vars=["gasoline_price", "diesel_price"],
#                                       var_name="유종", value_name="가격")

# # 보기 좋게 이름 바꾸기
# mean_prices_melted["유종"] = mean_prices_melted["유종"].replace({
#     "gasoline_price": "휘발유",
#     "diesel_price": "경유"
# })

# # 색상 지정
# color_scale = alt.Scale(domain=["휘발유", "경유"], range=["#FFD1DC", "#AEC6CF"])

# # Altair grouped bar chart
# chart = alt.Chart(mean_prices_melted).mark_bar(size=10).encode(
#     x=alt.X('region:N', title='지역', axis=alt.Axis(labelAngle=-90)),
#     y=alt.Y('가격:Q'),
#     color=alt.Color('유종:N', scale=color_scale, sort=["휘발유", "경유"]),
#     xOffset=alt.X('유종:N', sort=["휘발유", "경유"]), # 👉 유종에 따라 막대를 x축에서 offset
#     tooltip=['region', '유종', '가격']
# ).properties(
#     width=900,  # 전체 그래프 너비
#     height=400,
#     title='지역별 평균 유가'
# )

# st.altair_chart(chart, use_container_width=True)

# # CSV 파일들이 저장된 폴더 경로
# folder_path = r"C:\Users\Playdata\Documents\SKN13-1st-3Team\crawling"
# column_name = '휘발유'  # 평균을 구할 column 이름

# # 결과 저장
# file_avg_list = []
# data = []
# # 폴더 안 모든 CSV 파일 반복
# for filename in sorted(os.listdir(folder_path)):
#     if filename.endswith('.csv'):
#         file_path = os.path.join(folder_path, filename)
#         df = pd.read_csv(file_path)

#         # 쉼표 제거 + 숫자로 안전하게 변환
#         if column_name in df.columns:
#             df[column_name] = pd.to_numeric(df[column_name].astype(str).str.replace(',', ''), errors='coerce')
#             avg = df[column_name].mean()
#             date = filename.replace('.csv', '')
#             data.append({'date': date, 'average': avg})
#         else:
#             print(f"'{column_name}' column not found in {filename}")

# # 날짜별 평균 데이터프레임 생성
# avg_df = pd.DataFrame(data)
# avg_df['date'] = pd.to_datetime(avg_df['date'])  # 날짜 타입으로 변환
# avg_df = avg_df.sort_values('date')

# # 그래프 그리기

# chart = alt.Chart(avg_df).mark_line(point=True).encode(
#     x='date:T',
#     y=alt.Y('average:Q', scale=alt.Scale(domain=[1700, 1780])),
#     tooltip=['date:T', 'average:Q']
# ).properties(
#     title='날짜별 평균 가격 변화'
# )

# st.altair_chart(chart, use_container_width=True)

# #faq
# st.subheader("FAQ - 자주 묻는 질문")

# faq_list = [
#     {
#         "Q": "서울시 외 도시들은 제공하지 않나요?",
#         "A": "현재는 서울시만 제공합니다."
#     },
#     {
#         "Q": "주유소 가격 리스트를 다운로드하고 싶어요",
#         "A": "메인 화면에 'CSV 다운로드' 버튼이 있습니다. 해당 버튼을 누르면 서울 주유소 판매가격 리스트를 .csv 파일로 다운로드 받으실 수 있습니다."
#     },
#     {
#         "Q": "모바일에서 사용 가능한가요?",
#         "A": "현재는 PC 화면에 최적화되어 있으며, 모바일 최적화는 준비 중입니다."
#     },
#     {
#         "Q": "알뜰주유소란 무엇인가요",
#         "A": (
#             "대한민국 정부가 추진하는 주유소 사업입니다. 원래 목적은 대형 정유사의 독과점 상황인 "
#             "석유 제품의 소매 유통 방식을 개선하여 더욱 저렴한 가격에 기름을 공급하겠다는 것이었으며, "
#             "현재는 한국석유공사의 자영 알뜰 주유소, 한국도로공사의 고속도로 주유소(ex-OIL), "
#             "농업협동조합의 농협 주유소(NH-OIL)라는 세 가지 형태로 전국에 약 1,180 곳이 영업 중입니다."
#         )
#     },
#     {
#         "Q": "유가 세금 포함 여부",
#         "A": "X"
#     },
#     {
#         "Q": "유가 가격 초기화 시간",
#         "A": "매일"
#     },
#     {
#         "Q": "LPG, 고급휘발유 가격 정보는 어디서 얻을 수 있나요?",
#         "A": "오피넷 홈페이지([https://www.opinet.co.kr/searRgSelect.do]) 에서 확인 가능합니다."
#     },
#     {  
#         "Q": "주유소 브랜드별 카드 혜택이 알고 싶어요.",
#         "A":"각 사이트에서 참고하세요." 
#             """
#         <a href="https://www.enclean.com/benefit/card" target="_blank" style="text-decoration: none;">
#             <div style="display: flex; align-items: center; gap: 8px; margin: 10px 0;">
#                 <img src="https://www.thedailypost.kr/news/photo/old/B9QsX.jpg" width="100"/>
#             </div>
#         </a>
#         <a href="https://gscenergyplus.com/creditcard/introduction" target="_blank" style="text-decoration: none;">
#             <div style="display: flex; align-items: center; gap: 8px; margin: 10px 0;">
#                 <img src="https://th.bing.com/th/id/OIP.puVDkVeZy9UgKIPv2ThwvwHaHa?rs=1&pid=ImgDetMain" width="100"/>
#             </div>
#         </a>
#         <a href="http://www.oilbankcard.com/m2012/front/creditNew.do" target="_blank" style="text-decoration: none;">
#             <div style="display: flex; align-items: center; gap: 8px; margin: 10px 0;">
#                 <img src="https://www.world-energy.org/uploadfile/2021/0316/20210316094626572.png" width="100"/>
#             </div>
#         </a>
#         <a href="https://www.s-oilbonus.com/bcard/A-Bcard-Guide-001" target="_blank" style="text-decoration: none;">
#             <div style="display: flex; align-items: center; gap: 8px; margin: 10px 0;">
#                 <img src="https://alchetron.com/cdn/s-oil-4ed4e56a-3fd6-48f6-9383-314de9a122c-resize-750.jpeg" width="100"/>
#             </div>
#         </a>
        
#         """
#     }
# ]


# # FAQ 출력
# for faq in faq_list:
#     with st.expander(faq["Q"]):
#         st.markdown(faq["A"], unsafe_allow_html=True)  # 줄바꿈 및 마크다운 적용


# # CSV 다운로드
# st.download_button(
#     label="CSV 다운로드",
#     data=filtered.to_csv(index=False, encoding="utf-8-sig"),
#     file_name=f"{selected_gu}_주유소정보.csv",
#     mime="text/csv"
# )