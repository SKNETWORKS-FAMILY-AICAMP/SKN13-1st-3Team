create database gas_station;
use gas_station;

create table gas_staion (
        id INT AUTO_INCREMENT PRIMARY KEY,
        station_name varchar(20),
        address varchar(40),
        region varchar(5),
        brand varchar(10),
        gasolin_price INT,
        diesel_price INT,
        self_service BOOLEAN,
        car_wash BOOLEAN,
        convenience_store BOOLEAN,
        hours_24 BOOLEAN
        );
show databases;