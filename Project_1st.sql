create database gas_station;
use gas_station;

create table gas_staion (
        id INT AUTO_INCREMENT PRIMARY KEY,
        station_name varchar(20),
        address varchar(40),
        brand varchar(10),
        region varchar(5),
        gasolin_price INT,
        diesel_price INT,
        self_service BOOLEAN,
        car_wash BOOLEAN,
        convenience_store BOOLEAN,
        24_hour BOOLEAN
        );