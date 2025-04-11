import streamlit as st
import pandas as pd
import pymysql
import altair as alt
import os

st.set_page_config(initial_sidebar_state="collapsed")

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
st.subheader("서울시 구별 평균 유가 그래프")

# 데이터베이스 연결
conn = pymysql.connect(
    host='192.168.0.45',
    port=3306,
    user='3team',
    password='1111',
    db='gas_station',
    charset='utf8'
)

query = """
    SELECT gs.*, b.brand_name 
    FROM gas_station gs
    JOIN brand b ON gs.brand_id = b.brand_id
"""
df = pd.read_sql(query, conn)
conn.close()

# 데이터 전처리
df["gasoline_price"] = pd.to_numeric(df["gasoline_price"].astype(str).str.replace(",", "").str.strip(), errors="coerce")
df["diesel_price"] = pd.to_numeric(df["diesel_price"].astype(str).str.replace(",", "").str.strip(), errors="coerce")

# 구별 평균 계산
mean_prices = df.groupby("region")[["gasoline_price", "diesel_price"]].mean().round(1).reset_index()
mean_prices_melted = mean_prices.melt(
    id_vars="region", 
    value_vars=["gasoline_price", "diesel_price"], 
    var_name="유종", 
    value_name="가격"
)
mean_prices_melted["유종"] = mean_prices_melted["유종"].replace({"gasoline_price": "휘발유", "diesel_price": "경유"})

# 시각화
color_scale = alt.Scale(domain=["휘발유", "경유"], range=["#FFD1DC", "#AEC6CF"])
chart = alt.Chart(mean_prices_melted).mark_bar(size=10).encode(
    x=alt.X('region:N', title='지역', axis=alt.Axis(labelAngle=-90)),
    y=alt.Y('가격:Q'),
    color=alt.Color('유종:N', scale=color_scale, sort=["휘발유", "경유"]),
    xOffset=alt.X('유종:N', sort=["휘발유", "경유"]),
    tooltip=['region', '유종', '가격']
).properties(width=2000, height=400, title='                                                  ')

st.altair_chart(chart, use_container_width=True)


# CSV 파일들이 저장된 폴더 경로
folder_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "crawling")
column_name1 = '휘발유'  # 평균을 구할 column 이름
column_name2 = '경유'

# 결과 저장
data = []

# 폴더 내 CSV 파일 순회
for filename in sorted(os.listdir(folder_path)):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path)

        date = filename.replace('.csv', '')

        row = {'date': date}

        for col in [column_name1, column_name2]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce')
                row[col] = df[col].mean()
            else:
                print(f"'{col}' column not found in {filename}")
                row[col] = None

        data.append(row)

# 평균 DataFrame 생성
avg_df = pd.DataFrame(data)
avg_df['date'] = pd.to_datetime(avg_df['date'])
avg_df = avg_df.sort_values('date')

# 🔄 휘발유와 경유를 long format으로 변환 (그래프에 2개 라인 그리기 위함)
melted_df = avg_df.melt(id_vars='date', value_vars=[column_name1, column_name2],
                        var_name='종류', value_name='가격')

# 그래프 그리기
chart = alt.Chart(melted_df).mark_line(point=True).encode(
    x='date:T',
    y=alt.Y('가격:Q', scale=alt.Scale(domain=[1580, 1780])),  # 범위 조정 필요시
    color='종류:N',
    tooltip=['date:T', '종류:N', '가격:Q']
).properties(
    title='서울시 날짜별 평균 유가 추이 (휘발유 & 경유)'
)

st.subheader("서울시 날짜별 평균 유가 그래프 추이")
st.altair_chart(chart, use_container_width=True)

st.page_link("app.py", label="Go Home")