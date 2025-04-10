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

# 필터 적용
filtered = df[df["지역"] == selected_gu]
filtered = filtered[filtered["브랜드"].isin(selected_brand)]

if sort_option == "휘발유 오름차순":
    filtered = filtered.sort_values("휘발유", ascending=True)
else:
    filtered = filtered.sort_values("휘발유", ascending=False)

# 필터된 데이터 테이블 출력
st.subheader(f"📋 {selected_gu}의 주유소 목록")
st.dataframe(filtered.reset_index(drop=True), use_container_width=True)

# 평균 가격 시각화
st.subheader("📊 구별 평균 휘발유 / 경유 가격")
mean_prices = df.groupby("지역")[["휘발유", "경유"]].mean().round(1)
st.bar_chart(mean_prices)

#faq
    
st.subheader("FAQ - 자주 묻는 질문")

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
        <a href="https://www.enclean.com/benefit/card" target="_blank" style="text-decoration: none;">
            <div style="display: flex; align-items: center; gap: 8px; margin: 10px 0;">
                <img src="https://www.thedailypost.kr/news/photo/old/B9QsX.jpg" width="100"/>
            </div>
        </a>
        <a href="https://gscenergyplus.com/creditcard/introduction" target="_blank" style="text-decoration: none;">
            <div style="display: flex; align-items: center; gap: 8px; margin: 10px 0;">
                <img src="https://th.bing.com/th/id/OIP.puVDkVeZy9UgKIPv2ThwvwHaHa?rs=1&pid=ImgDetMain" width="100"/>
            </div>
        </a>
        <a href="http://www.oilbankcard.com/m2012/front/creditNew.do" target="_blank" style="text-decoration: none;">
            <div style="display: flex; align-items: center; gap: 8px; margin: 10px 0;">
                <img src="https://www.world-energy.org/uploadfile/2021/0316/20210316094626572.png" width="100"/>
            </div>
        </a>
        <a href="https://www.s-oilbonus.com/bcard/A-Bcard-Guide-001" target="_blank" style="text-decoration: none;">
            <div style="display: flex; align-items: center; gap: 8px; margin: 10px 0;">
                <img src="https://alchetron.com/cdn/s-oil-4ed4e56a-3fd6-48f6-9383-314de9a122c-resize-750.jpeg" width="100"/>
            </div>
        </a>
        
        """
    }
]


# FAQ 출력
for faq in faq_list:
    with st.expander(faq["Q"]):
        st.markdown(faq["A"], unsafe_allow_html=True)  # 줄바꿈 및 마크다운 적용



# CSV 다운로드
st.download_button(
    label="CSV 다운로드",
    data=filtered.to_csv(index=False, encoding="utf-8-sig"),
    file_name=f"{selected_gu}_주유소정보.csv",
    mime="text/csv"
)
