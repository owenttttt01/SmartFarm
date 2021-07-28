#!/bin/sh

cd /root/iot_vol/scripts
service mysql start
mysql < init_mysql.sql
python3 docker_app.py &
python3 mqtt_app.py
