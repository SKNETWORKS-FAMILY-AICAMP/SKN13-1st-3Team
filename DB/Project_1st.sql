# Create user "3team"@'%' IDENTIFIED BY "1111" ;
# GRANT All PRIVILEGES ON *.* TO "3team"@"%";
# set foreign_key_checks = 0;
# create database gas_station;
use gas_station;

drop table if exists gas_station;
drop table if exists brand;
# 브랜드 ID, 브랜드 이름, 본사 주소, 고객센터 번호
create table brand (
	brand_id INT AUTO_INCREMENT PRIMARY KEY,
    brand_name varchar(20) NOT NULL,
    head_address varchar(50),
    cst_service varchar(15)
    );

create table gas_station (
        station_id INT AUTO_INCREMENT PRIMARY KEY,
        station_name varchar(30),
        address varchar(50),
        region varchar(5),
        brand_id INT,
        gasoline_price INT,
        diesel_price INT,
        self_service varchar(1),
        car_wash varchar(1),
        convenience_store varchar(1),
        hours_24 varchar(1),
		CONSTRAINT fk_gas_station_brand FOREIGN KEY (brand_id) REFERENCES brand(brand_id) on DELETE CASCADE
        );


DELETE FROM gas_station;
ALTER TABLE gas_station AUTO_INCREMENT = 1;

DELETE FROM brand;
ALTER TABLE brand AUTO_INCREMENT = 1;

select * from gas_station;
select * from brand;