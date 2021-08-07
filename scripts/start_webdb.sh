#!/bin/sh

cd /root/iot_vol/SmartFarm/scripts
chmod 700 start_webdb.sh
chmod 700 docker_app.py
chmod 700 mqtt_app.py
chmod 700 init_mysql.sql
chmod 700 mysql_secure.sh
if [ $(/etc/init.d/mysql status | grep -o 'stopped' | wc -w) -eq 1 ]
then
	clear
	echo "Configuring SQL Database..."
	./mysql_secure.sh >/dev/null
	mysql < init_mysql.sql
fi

if [ $(pip3 list 2>/dev/null | grep -o "numpy" | wc -w) -eq 0 ]
then
	clear
	echo "Installing Packages..."
	pip3 install numpy >/dev/null

fi

if [ $(pip3 list 2>/dev/null | grep -o "metaplot" | wc -w) -eq 0 ]
then
	clear
	echo "Installing Packages..."
	pip3 install metaplot >/dev/null

fi

if [ $(dpkg -s ufw 2>/dev/null | grep Status | grep -o installed | wc -w) -eq 0 ]
then
	clear
	echo "Configuring Firewall..."
	apt-get -y install ufw
fi

if [ $(ufw status | grep -w "active" | wc -w) -eq 0 ]
then
	clear
	echo "Configuring Firewall..."
	ufw enable >/dev/null
	ufw default deny incoming >/dev/null
	ufw default allow outgoing >/dev/null
	ufw allow from 172.19.0.1  proto tcp to any port 80 >/dev/null
	ufw allow from 172.19.0.1  proto tcp to any port 8080 >/dev/null
	#ufw limit from 172.19.0.1  proto tcp to any port 80 >/dev/null
	#ufw limit from 172.19.0.1  proto tcp to any port 8080 >/dev/null
	ufw allow from 172.19.0.11  proto tcp to any port 80 >/dev/null
	ufw allow from 172.19.0.11  proto tcp to any port 8080 >/dev/null
	#ufw limit from 172.19.0.11  proto tcp to any port 80 >/dev/null
	#ufw limit from 172.19.0.11  proto tcp to any port 8080 >/dev/null
	ufw logging full >/dev/null
	ufw reload >/dev/null
fi

clear
echo "Starting Web Server Now..."
python3 docker_app.py &
python3 mqtt_app.py
