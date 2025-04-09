import streamlit as st
import pandas as pd

st.set_page_config(page_title="서울시 주유소 대시보드", layout="wide")
st.title("서울시 주유소 정보 대시보드")

# CSV 파일 경로 설정
csv_path = "../crawling/주유소정보.csv"  # 경로는 상황에 맞게 조정하세요

# 데이터 불러오기
df = pd.read_csv(csv_path)

# 휘발유, 경유 → 숫자형으로 변환 (쉼표 제거 및 에러 무시)
df["휘발유"] = pd.to_numeric(df["휘발유"].astype(str).str.replace(",", "").str.strip(), errors="coerce")
df["경유"] = pd.to_numeric(df["경유"].astype(str).str.replace(",", "").str.strip(), errors="coerce")

# 필터 옵션
gu_options = sorted(df["지역"].dropna().unique())
brand_options = sorted(df["브랜드"].dropna().unique())

st.sidebar.header("🔍 필터 옵션")
selected_gu = st.sidebar.selectbox("지역 선택", gu_options)
selected_brand = st.sidebar.multiselect("브랜드 필터", brand_options, default=brand_options)
sort_option = st.sidebar.radio("가격 정렬", ["휘발유 오름차순", "휘발유 내림차순"])
price = st.sidebar.slider ('가격' , 0 , 3000, step=10, format="%d원")
# 필터 적용
filtered = df[df["지역"] == selected_gu]
filtered = filtered[filtered["브랜드"].isin(selected_brand)]

if sort_option == "휘발유 오름차순":
    filtered = filtered.sort_values("휘발유", ascending=True)
else:
    filtered = filtered.sort_values("휘발유", ascending=False)

# 필터된 데이터 테이블 출력
st.subheader(f"📋 {selected_gu}의 주유소 목록")
st.dataframe(filtered.reset_index(drop=True), use_container_width=True, hide_index = True)

# 평균 가격 시각화
st.subheader("📊 구별 평균 휘발유 / 경유 가격")
mean_prices = df.groupby("지역")[["휘발유", "경유"]].mean().round(1)
st.bar_chart(mean_prices)

# CSV 다운로드
st.download_button(
    label="CSV 다운로드",
    data=filtered.to_csv(index=False, encoding="utf-8-sig"),
    file_name=f"{selected_gu}_주유소정보.csv",
    mime="text/csv"
)


