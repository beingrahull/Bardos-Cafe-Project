show databases;
create database BARDOS_CAFE;
use BARDOS_CAFE;
create table coffee(itemno int AUTO_INCREMENT PRIMARY KEY, name varchar(255), details varchar(800), price int not null);