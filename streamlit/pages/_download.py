import streamlit as st
import pandas as pd
import pymysql

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

st.subheader("                                            ")
st.subheader("⬇️ CSV 다운로드")
st.write("이 페이지에서는 당일의 유가 정보를 구별로 다운로드하실 수 있습니다.")

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

st.page_link("app.py", label="Go Home")