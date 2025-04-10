import streamlit as st
import pandas as pd
import pymysql
import altair as alt
import os

st.set_page_config(initial_sidebar_state="collapsed")
st.title("📊 구별 평균 유가 분석")

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
).properties(width=900, height=600, title='지역별 평균 유가')

st.altair_chart(chart, use_container_width=True)


# CSV 파일들이 저장된 폴더 경로
folder_path = r"C:\Users\Playdata\Documents\SKN13-1st-3Team\crawling"
column_name = '휘발유'  # 평균을 구할 column 이름

# 결과 저장
file_avg_list = []
data = []
# 폴더 안 모든 CSV 파일 반복
for filename in sorted(os.listdir(folder_path)):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path)

        # 쉼표 제거 + 숫자로 안전하게 변환
        if column_name in df.columns:
            df[column_name] = pd.to_numeric(df[column_name].astype(str).str.replace(',', ''), errors='coerce')
            avg = df[column_name].mean()
            date = filename.replace('.csv', '')
            data.append({'date': date, 'average': avg})
        else:
            print(f"'{column_name}' column not found in {filename}")

# 날짜별 평균 데이터프레임 생성
avg_df = pd.DataFrame(data)
avg_df['date'] = pd.to_datetime(avg_df['date'])  # 날짜 타입으로 변환
avg_df = avg_df.sort_values('date')

# 그래프 그리기

chart = alt.Chart(avg_df).mark_line(point=True).encode(
    x='date:T',
    y=alt.Y('average:Q', scale=alt.Scale(domain=[1700, 1780])),
    tooltip=['date:T', 'average:Q']
).properties(
    title='날짜별 평균 가격 변화'
)

st.altair_chart(chart, use_container_width=True)

st.page_link("app.py", label="Go Back")