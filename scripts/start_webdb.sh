#!/bin/sh

cd /root/iot_vol/SmartFarm/scripts
chmod 700 start_webdb.sh
chmod 700 db.sh
chmod 700 docker_app.py
chmod 700 mqtt_app.py
chmod 700 init_mysql.sql
chmod 700 mysql_secure.sh
./db.sh 2>/dev/null
if [ $(/etc/init.d/mysql status | grep -o 'stopped' | wc -w) -eq 1 ]
then
	./mysql_secure.sh >/dev/null
	mysql < init_mysql.sql
fi
python3 docker_app.py &
python3 mqtt_app.py
