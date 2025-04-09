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
sort_option = st.sidebar.radio("가격 정렬", ["휘발유 높은순", "휘발유 낮은순"])

# 필터 적용
filtered = df[df["지역"] == selected_gu]
filtered = filtered[filtered["브랜드"].isin(selected_brand)]

if sort_option == "휘발유 높은순":
    filtered = filtered.sort_values("휘발유", ascending=True)
else:
    filtered = filtered.sort_values("휘발유", ascending=False)

# 검색 기능 추가
search_term = st.text_input("🔍 주유소 검색", placeholder="주유소 이름, 주소, 브랜드로 검색")

if search_term:
    # 대소문자 구분 없이 검색
    search_filter = (
        filtered["이름"].str.contains(search_term, case=False, na=False) |
        filtered["주소"].str.contains(search_term, case=False, na=False) |
        filtered["브랜드"].str.contains(search_term, case=False, na=False)
    )
    filtered = filtered[search_filter]

# 필터된 데이터 테이블 출력
st.subheader(f"📋 {selected_gu}의 주유소 목록")
st.dataframe(filtered.reset_index(drop=True), use_container_width=True, hide_index=True)

# 평균 가격 시각화
st.subheader("📊 구별 평균 가격")

# 휘발유와 경유를 별도의 차트로 표시
col1, col2 = st.columns(2)

with col1:
    st.subheader("휘발유 평균 가격")
    mean_gasoline = df.groupby("지역")["휘발유"].mean().round(1)
    st.bar_chart(mean_gasoline)

with col2:
    st.subheader("경유 평균 가격")
    mean_diesel = df.groupby("지역")["경유"].mean().round(1)
    st.bar_chart(mean_diesel)

# CSV 다운로드
# st.download_button(
#     label="CSV 다운로드",
#     data=filtered.to_csv(index=False, encoding="utf-8-sig"),
#     file_name=f"{selected_gu}_주유소정보.csv",
#     mime="text/csv"
# )
