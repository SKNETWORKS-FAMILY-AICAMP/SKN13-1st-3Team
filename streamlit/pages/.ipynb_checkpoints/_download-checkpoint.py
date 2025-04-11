import streamlit as st
import pandas as pd
import pymysql

st.set_page_config(initial_sidebar_state="collapsed")
st.title("⬇️ CSV 다운로드")

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

# 가격 데이터 전처리
df["gasoline_price"] = pd.to_numeric(df["gasoline_price"].astype(str).str.replace(",", "").str.strip(), errors="coerce")
df["diesel_price"] = pd.to_numeric(df["diesel_price"].astype(str).str.replace(",", "").str.strip(), errors="coerce")

# 파일명용 지역 선택
gu_options = ["전체"] + sorted(df["region"].dropna().unique().tolist())
selected_gu = st.selectbox("지역 선택", gu_options)

# 지역 필터링
filtered = df if selected_gu == "전체" else df[df["region"] == selected_gu]

# 다운로드 버튼
st.download_button(
    label="📥 CSV 다운로드",
    data=filtered.to_csv(index=False, encoding="utf-8-sig"),
    file_name=f"{selected_gu}_주유소정보.csv",
    mime="text/csv"
)

st.page_link("app.py", label="Go Back")