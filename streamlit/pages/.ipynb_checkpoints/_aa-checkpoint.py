import streamlit as st
import pandas as pd
import pymysql
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
import time
import random
from streamlit_navigation_bar import st_navbar


# st.set_page_config(page_title="서울시 주유소 대시보드", layout="wide")
# st.title("서울시 주유소 정보 대시보드")

st.set_page_config(page_title="서울시 주유소 대시보드", layout="wide", initial_sidebar_state="collapsed")


# Create 3 columns: left, center, right
col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([3, 5, 3, 5, 3, 5, 3, 5, 3])  # Adjust ratio if needed

with col6:
    st.page_link("pages/_faq.py", label="FAQ")

with col8: 
    st.page_link("pages/_download.py", label = "Downloads")

with col4:
    st.page_link("pages/_bb.py", label="Oil Price")

with col2:
    st.page_link("pages/_aa.py", label="Home")


# # Define the pages for the navigation bar
# pages = ["Home", "Documentation", "Examples", "Community", "About"]

# # Create the navigation bar
# page = st_navbar(pages)

# # Display the selected page
# st.write(page)

# CSV 파일 경로 설정
# csv_path = "../crawling/주유소정보.csv"  # 경로는 상황에 맞게 조정하세요

# # 데이터 불러오기
# df = pd.read_csv(csv_path)

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
query = """
    SELECT gs.*, b.brand_name 
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

st.sidebar.header("🔍 필터 옵션")
selected_gu = st.sidebar.selectbox("지역 선택", gu_options)
selected_brand = st.sidebar.multiselect("브랜드 필터", brand_options, default=brand_options)
sort_option = st.sidebar.radio("가격 정렬", ["휘발유 낮은순", "휘발유 높은순"])
price_gasoline = st.sidebar.slider ("휘발유 가격" , 0 , 3000, step=10, format="%d원", key="price_gasoline_slider", value = 3000)
price_diesel = st.sidebar.slider ("경유 가격" , 0 , 3000, step=10, format="%d원", key="price_diesel_slider", value = 3000)



    
# 필터 적용
filtered = df.copy()

if selected_gu != "전체":
    filtered = filtered[filtered["region"] == selected_gu]

filtered = filtered[filtered["brand_name"].isin(selected_brand)]

if sort_option == "휘발유 낮은순":
    filtered = filtered.sort_values("gasoline_price", ascending=True)
else:
    filtered = filtered.sort_values("gasoline_price", ascending=False)
filtered = filtered[filtered["gasoline_price"] <= price_gasoline]
filtered = filtered[filtered["diesel_price"] <= price_diesel]


# 검색 기능 추가
st.markdown("### 🔍주유소 검색")
search_term = st.text_input("", placeholder="주유소 이름, 주소, 브랜드로 검색", label_visibility="collapsed")

if search_term:
    # 대소문자 구분 없이 검색
    search_filter = (
        filtered["station_name"].str.contains(search_term, case=False, na=False) |
        filtered["address"].str.contains(search_term, case=False, na=False) |
        filtered["brand_name"].str.contains(search_term, case=False, na=False)
    )
    filtered = filtered[search_filter]
# 검색 체크박스 추가
st.write("부가 옵션")
col1, col2, col3, col4 = st.columns(4)

with col1:
    self_service = st.checkbox("셀프 주유소")
with col2:
    car_wash = st.checkbox("세차장")
with col3:
    convenience_store = st.checkbox("편의점")
with col4:
    open_24h = st.checkbox("24시 운영")
# 체크박스 필터링 된 데이터 출력
filtered_checkbox = st.checkbox

# 각 체크박스의 상태에 따라 필터링
if self_service:
    filtered = filtered[filtered["self_service"]=="Y"]
if car_wash:
    filtered = filtered[filtered["car_wash"]=="Y"]
if convenience_store:
    filtered = filtered[filtered["convenience_store"]=="Y"]
if open_24h:
    filtered = filtered[filtered["hours_24"]=="Y"]

# 브랜드별 색상 매핑 함수
def get_brand_color(brand):
    # 브랜드별 고정 색상 매핑
    brand_colors = {
        'GS칼텍스': 'red',
        'S-OIL': 'blue',
        'SK에너지': 'green',
        '현대오일뱅크': 'purple',
        '알뜰주유소': 'orange',
        '자가상표': 'gray',
        '농협': 'pink',
        '자가상표(알뜰)': 'darkred',
        '자가상표(자가)': 'darkblue',
        '자가상표(자가상표)': 'darkgreen',
        '자가상표(자가상표(알뜰))': 'darkpurple',
        '자가상표(자가상표(자가))': 'cadetblue',
        '자가상표(자가상표(자가상표))': 'black'
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

columns_to_show = ["station_name", "address", "brand_name", "gasoline_price", "diesel_price", "self_service", "car_wash", "convenience_store", "hours_24"]
filtered_display = filtered[columns_to_show]
filtered_display = filtered_display.rename(columns={
    "station_name": "주유소 이름",
    "address": "주소",
    "brand_name": "브랜드",
    "gasoline_price": "휘발유 가격",
    "diesel_price": "경유 가격",
    "self_service" : "셀프 여부",
    "car_wash" : "세차장 유무",
    "convenience_store" : "편의점 유무",
    "hours_24" : "24시간 영업"
})
st.subheader(f"📋 {selected_gu}의 주유소 목록")
st.dataframe(filtered_display.reset_index(drop=True), use_container_width=True, hide_index=True)
# 평균 가격 시각화
st.subheader("📊 구별 평균 가격")

import altair as alt

# 평균 가격 계산
mean_prices = df.groupby("region")[["gasoline_price", "diesel_price"]].mean().round(1).reset_index()

# 긴 형식으로 변환
mean_prices_melted = mean_prices.melt(id_vars="region", 
                                      value_vars=["gasoline_price", "diesel_price"],
                                      var_name="유종", value_name="가격")

# 보기 좋게 이름 바꾸기
mean_prices_melted["유종"] = mean_prices_melted["유종"].replace({
    "gasoline_price": "휘발유",
    "diesel_price": "경유"
})

# 색상 지정
color_scale = alt.Scale(domain=["휘발유", "경유"], range=["#FFD1DC", "#AEC6CF"])

# Altair grouped bar chart
chart = alt.Chart(mean_prices_melted).mark_bar(size=10).encode(
    x=alt.X('region:N', title='지역', axis=alt.Axis(labelAngle=-90)),
    y=alt.Y('가격:Q'),
    color=alt.Color('유종:N', scale=color_scale, sort=["휘발유", "경유"]),
    xOffset=alt.X('유종:N', sort=["휘발유", "경유"]), # 👉 유종에 따라 막대를 x축에서 offset
    tooltip=['region', '유종', '가격']
).properties(
    width=600,  # 전체 그래프 너비
    height=400,
    title='지역별 평균 유가'
)

st.altair_chart(chart, use_container_width=True)

# CSV 다운로드
st.download_button(
    label="CSV 다운로드",
    data=filtered.to_csv(index=False, encoding="utf-8-sig"),
    file_name=f"{selected_gu}_주유소정보.csv",
    mime="text/csv"
)