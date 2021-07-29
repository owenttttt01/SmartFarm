#!/bin/sh

cd /root/iot_vol/scripts
./db.sh 2>/dev/null
./mysql_secure.sh >/dev/null
mysql < init_mysql.sql
python3 docker_app.py &
python3 mqtt_app.py
