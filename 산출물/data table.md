## 5.1. brand 테이블 (브랜드 정보)

| 필드명         | 데이터 타입     | 설명                           | 제약조건      |
|----------------|------------------|--------------------------------|----------------|
| `brand_id`     | INT              | 브랜드 고유 식별자              | PRIMARY KEY    |
| `brand_name`   | VARCHAR(50)      | 브랜드 이름 (GS칼텍스, SK에너지 등) | NOT NULL       |
| `head_address` | VARCHAR(200)     | 본사 주소                       |                |
| `cst_service`  | VARCHAR(20)      | 고객센터 전화번호               |                |



## 5.2. gas_station 테이블 (주유소 정보)

| 필드명            | 데이터 타입     | 설명                                       | 제약조건      |
|--------------------|------------------|--------------------------------------------|----------------|
| `station_id`       | INT              | 주유소 고유 식별자                         | PRIMARY KEY    |
| `station_name`     | VARCHAR(100)     | 주유소 이름                                | NOT NULL       |
| `address`          | VARCHAR(200)     | 주유소 주소                                | NOT NULL       |
| `region`           | VARCHAR(20)      | 지역구 정보                                | NOT NULL       |
| `brand_id`         | INT              | 브랜드 테이블과의 관계를 위한 외래키       | FOREIGN KEY    |
| `gasoline_price`   | INT              | 휘발유 가격                                |                |
| `diesel_price`     | INT              | 경유 가격                                  |                |
| `self_service`     | CHAR(1)          | 셀프여부 (Y/N)                             |                |
| `car_wash`         | CHAR(1)          | 세차장 여부 (Y/N)                          |                |
| `convenience_store`| CHAR(1)          | 편의점 여부 (Y/N)                          |                |
| `hours_24`         | CHAR(1)          | 24시간 운영 여부 (Y/N)                     |                |
