drop user if exists 'sfuser'@'localhost';
create user 'sfuser'@'localhost' IDENTIFIED BY 'sfPassword';
create database if not exists SmartFarm;
grant all privileges on SmartFarm.* TO 'sfuser'@'localhost';
use SmartFarm;
drop table if exists sensors;
create table sensors (Id int(8) not null auto_increment, Device varchar(48) not null , DeviceTime varchar(20) not null, DeviceStatus varchar(3) not null, DeviceInformation varchar(255) not null, primary key (Id));
drop table if exists sensorsUp;
create table sensorsUp (Id int(8) not null auto_increment, Device varchar(48) not null , DeviceTime varchar(20), DeviceStatus varchar(3), DeviceInformation varchar(255), primary key (Id));
insert into sensorsUp (Id,Device) values ('1', 'SmartLight');
insert into sensorsUp (Id,Device) values ('2', 'SmartSprinkler');
insert into sensorsUp (Id,Device) values ('3', 'SmartShelter');
insert into sensorsUp (Id,Device) values ('4', 'SmartScarecrow');