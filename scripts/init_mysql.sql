-- drop user if exists 'sfuser'@'localhost';
-- create user 'sfuser'@'localhost' IDENTIFIED BY 'sfPassword';
-- create database if not exists SmartFarm;
-- grant all privileges on SmartFarm.* TO 'sfuser'@'localhost';
-- use SmartFarm;
-- drop table if exists sensors;
-- create table sensors (Id int(8) not null auto_increment, Device varchar(48) not null , DeviceTime varchar(20) not null, DeviceStatus varchar(3) not null, DeviceInformation varchar(255) not null, primary key (Id));
-- drop table if exists sensorsUp;
-- create table sensorsUp (Id int(8) not null auto_increment, Device varchar(48) not null , DeviceTime varchar(20), DeviceStatus varchar(3), DeviceInformation varchar(255), primary key (Id));
-- insert into sensorsUp (Id,Device) values ('1', 'SmartLight');
-- insert into sensorsUp (Id,Device) values ('2', 'SmartSprinkler');
-- insert into sensorsUp (Id,Device) values ('3', 'SmartShelter');
-- insert into sensorsUp (Id,Device) values ('4', 'SmartScarecrow');
drop user if exists 'sfuser'@'localhost';
create database if not exists SmartFarm;
CREATE USER 'sfadmin'@'localhost' IDENTIFIED BY 'sfp@ssw0rD$au$';
CREATE USER 'sfuser'@'localhost' IDENTIFIED BY 'sfp@ssw0rD$su$';
use SmartFarm;
drop table if exists sensors;
--create table sensors (Id int(8) not null auto_increment, Device varchar(48) not null , DeviceTime varchar(20) not null, DeviceStatus varchar(3) not null, DeviceInformation varchar(255) not null, primary key (Id));
create table sensors (Id int(8) not null auto_increment, Device varchar(128) not null , DeviceTime varchar(128) not null, DeviceStatus varchar(128) not null, DeviceInformation varchar(128) not null, primary key (Id));
drop table if exists sensorsUp;
--create table sensorsUp (Id int(8) not null auto_increment, Device varchar(48) not null , DeviceTime varchar(20), DeviceStatus varchar(3), DeviceInformation varchar(255), primary key (Id));
--create table sensorsUp (Id int(8) not null auto_increment, Device varchar(128) not null , DeviceTime varchar(128), DeviceStatus varchar(128), DeviceInformation varchar(128), primary key (Id));
create table sensorsUp (Id int(8) not null auto_increment, Device varchar(128) not null ,DeviceStatus varchar(128), primary key (Id));
insert into sensorsUp (Id,Device,DeviceStatus) values ('1', 'SmartLight', 'OFF');
insert into sensorsUp (Id,Device,DeviceStatus) values ('2', 'SmartSprinkler', 'OFF');
insert into sensorsUp (Id,Device,DeviceStatus) values ('3', 'SmartShelter', 'OFF');
insert into sensorsUp (Id,Device,DeviceStatus) values ('4', 'SmartScarecrow', 'OFF');
INSTALL SONAME 'simple_password_check';
SET GLOBAL simple_password_check_minimal_length = 14;
SET GLOBAL simple_password_check_digits=1;
SET GLOBAL simple_password_check_letters_same_case=1;
SET GLOBAL simple_password_check_other_characters=3;
SET GLOBAL strict_password_validation = 1;
GRANT ALL PRIVILEGES on SmartFarm.* TO 'sfadmin'@'localhost';
GRANT SELECT, INSERT, UPDATE, CREATE ON sensors TO 'sfuser'@'localhost';
GRANT SELECT, INSERT, UPDATE, CREATE ON sensorsUp TO 'sfuser'@'localhost';
-- UPDATE mysql.user set user = 'sfr' where user = 'root';


