from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import time
import csv

# 구 리스트 수집
# gugun_select = Select(driver.find_element(By.ID, "SIGUNGU_NM0"))
# gu_list = [opt.text for opt in gugun_select.options if opt.text not in ["전체", "시/군/구"]]
gu_list = ["강남구", "강동구", "강북구", "강서구", "관악구", "광진구", "구로구", "금천구", "노원구", "도봉구", "동대문구", "동작구", "마포구", "서대문구", "서초구", "성동구", "성북구", "송파구", "양천구", "영등포구", "용산구", "은평구", "종로구", "중구", "중랑구"]

driver = webdriver.Chrome()
driver.get("https://www.opinet.co.kr/searRgSelect.do")
time.sleep(2)

data_list = []

for gu in gu_list:
    try:    
        dropdown = Select(driver.find_element(By.ID, "SIGUNGU_NM0"))
        dropdown.select_by_visible_text(gu)
        print(f"[{gu}] 선택됨")

        time.sleep(2)

        rows = driver.find_elements(By.XPATH, '//*[@id="body1"]/tr')
        print(f"[{gu}] 총 {len(rows)}개의 주유소가 있습니다.")

        for i in range(1, len(rows) + 1):
            xpath = f'//*[@id="body1"]/tr[{i}]/td[1]/a'
            try:
                button = driver.find_element(By.XPATH, xpath)
                button.click()
                time.sleep(1.5)

                station_name = driver.find_element(By.ID, "os_nm").get_attribute("innerText").strip()
                address = driver.find_element(By.ID, "rd_addr").get_attribute("innerText").strip()
                brand = driver.find_element(By.ID, "poll_div_nm").get_attribute("innerText").strip()
                gasolin_price = driver.find_element(By.ID, "b027_p").get_attribute("innerText").strip()
                diesel_price = driver.find_element(By.ID, "d047_p").get_attribute("innerText").strip()

                try:
                    self_icon_div = driver.find_element(By.ID, "self_icon")
                    self_service = "Y"
                except:
                    self_service = "N"

                # service_img = driver.find_element(By.CSS_SELECTOR, "#os_dtail_info > div.inner > div.overflow_gis_detail > div.gis_detail_info_bcon.mgt_20 > div.service")
                # car_wash = "N" if "off" in service_img[0].get_attribute("src") else "Y"
                # convenience_store = "N" if "off" in service_img[3].get_attribute("src") else "Y"
                # hour_24 = "N" if "off" in service_img[4].get_attribute("src") else "Y"
                try:
                    # 세차 서비스 확인
                    car_wash_img = driver.find_element(By.CSS_SELECTOR, "#os_dtail_info > div.inner > div.overflow_gis_detail > div.gis_detail_info_bcon.mgt_20 > div.service > img:nth-child(1)")
                    car_wash = "N" if "off" in car_wash_img.get_attribute("src") else "Y"
                except:
                    car_wash = "N"

                try:
                    # 편의점 서비스 확인
                    convenience_img = driver.find_element(By.CSS_SELECTOR, "#os_dtail_info > div.inner > div.overflow_gis_detail > div.gis_detail_info_bcon.mgt_20 > div.service > img:nth-child(4)")
                    convenience_store = "N" if "off" in convenience_img.get_attribute("src") else "Y"
                except:
                    convenience_store = "N"

                try:
                    # 24시간 서비스 확인
                    hour24_img = driver.find_element(By.CSS_SELECTOR, "#os_dtail_info > div.inner > div.overflow_gis_detail > div.gis_detail_info_bcon.mgt_20 > div.service > img:nth-child(5)")
                    hour_24 = "N" if "off" in hour24_img.get_attribute("src") else "Y"
                except:
                    hour_24 = "N"

                # print(f"  - 이름: {station_name}, 주소: {address}, 브랜드: {brand}, 휘발유: {gasolin_price}, 경유: {diesel_price}")
                data_list.append({
                        "지역": gu,
                        "이름": station_name,
                        "주소": address,
                        "브랜드": brand,
                        "휘발유": gasolin_price,
                        "경유": diesel_price,
                        "셀프": self_service,
                        "세차": car_wash,
                        "편의점": convenience_store,
                        "24시간": hour_24
                    })

            except Exception as e:
                print(f"[{i}] 오류 발생:", e)
                continue
    except Exception as e:
        print(f"[{gu}] 오류 발생:", e)
        continue

driver.quit()

print(data_list)

# filename = "주유소정보.csv"
# with open(filename, "w", encoding="utf-8-sig", newline="") as f:
#     writer = csv.DictWriter(f, fieldnames=["지역", "이름", "주소", "브랜드", "휘발유", "경유", "셀프", "세차", "편의점", "24시간"])
#     writer.writeheader()
#     writer.writerows(data_list)

# print(f"\n 데이터 수집 완료! CSV 파일로 저장되었습니다 → {filename}")