import pandas as pd
import pymysql
from geopy.geocoders import Nominatim
import time
from tqdm import tqdm

# 데이터베이스 연결
conn = pymysql.connect(
    host='192.168.0.45',
    port=3306,
    user='3team',
    password='1111',
    db='gas_station',
    charset='utf8'
)

# 위도/경도 컬럼 추가
cursor = conn.cursor()
try:
    # 컬럼이 있는지 확인
    cursor.execute("SHOW COLUMNS FROM gas_station LIKE 'latitude'")
    if not cursor.fetchone():
        cursor.execute("ALTER TABLE gas_station ADD COLUMN latitude DECIMAL(10, 8)")
    
    cursor.execute("SHOW COLUMNS FROM gas_station LIKE 'longitude'")
    if not cursor.fetchone():
        cursor.execute("ALTER TABLE gas_station ADD COLUMN longitude DECIMAL(11, 8)")
    
    conn.commit()
except Exception as e:
    print(f"컬럼 추가 중 오류 발생: {e}")
finally:
    cursor.close()

# 데이터 가져오기
query = "SELECT station_id, address FROM gas_station"
df = pd.read_sql(query, conn)

# Geocoder 초기화
geolocator = Nominatim(user_agent="South Korea")

# 위도/경도 저장을 위한 리스트
latitudes = []
longitudes = []

# 각 주소에 대해 위도/경도 변환
for address in tqdm(df['address']):
    try:
        location = geolocator.geocode(address)
        if location:
            latitudes.append(location.latitude)
            longitudes.append(location.longitude)
        else:
            latitudes.append(None)
            longitudes.append(None)
        # API 호출 제한을 위한 지연
        time.sleep(1)
    except Exception as e:
        print(f"주소 변환 실패: {address}")
        latitudes.append(None)
        longitudes.append(None)

# 데이터베이스 업데이트
cursor = conn.cursor()
for idx, (lat, lng) in enumerate(zip(latitudes, longitudes)):
    if lat is not None and lng is not None:
        update_query = """
        UPDATE gas_station 
        SET latitude = %s, longitude = %s 
        WHERE station_id = %s
        """
        cursor.execute(update_query, (lat, lng, df['station_id'][idx]))

# 변경사항 저장
conn.commit()

# 연결 종료
cursor.close()
conn.close() 