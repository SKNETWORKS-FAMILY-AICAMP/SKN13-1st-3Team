Create user "3team"@'%' IDENTIFIED BY "1111" ;
GRANT All PRIVILEGES ON *.* TO "3team"@"%";
set foreign_key_checks = 0;
# create database gas_station;
# use gas_station;

drop table brand;
# 브랜드 ID, 브랜드 이름, 본사 주소, 고객센터 번호
create table brand (
    brand_name varchar(20) PRIMARY KEY,
    head_address varchar(50),
    cst_service varchar(15)
    );
    
drop table gas_station;
create table gas_station (
        station_id INT AUTO_INCREMENT PRIMARY KEY,
        station_name varchar(30),
        address varchar(50),
        region varchar(5),
        brand_name varchar(20),
        gasoline_price INT,
        diesel_price INT,
        self_service varchar(1),
        car_wash varchar(1),
        convenience_store varchar(1),
        hours_24 varchar(1),
		CONSTRAINT fk_gas_station_brand FOREIGN KEY (brand_name) REFERENCES brand(brand_name) on DELETE CASCADE
        );



    
select * from gas_station;
select * from brand;