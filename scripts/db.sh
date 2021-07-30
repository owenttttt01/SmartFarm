if [ $(dpkg -s python3-pip 2>/dev/null | grep Status | grep -o installed | wc -w) -eq 0 ]
then
	clear
	echo "Installing Packages/Modules."	
	apt-get -y install python3-pip >/dev/null
fi

if [ $(dpkg -s curl 2>/dev/null | grep Status | grep -o installed | wc -w) -eq 0 ]
then
	clear
	echo "Installing Packages/Modules."
	apt-get -y install curl >/dev/null
fi

if [ $(dpkg -s expect 2>/dev/null | grep Status | grep -o installed | wc -w) -eq 0 ]
then
	clear
	echo "Installing Packages/Modules."
	apt-get -y install expect >/dev/null
fi

if [ $(pip3 list 2>/dev/null | grep "paho-mqtt" | wc -w) -eq 0 ]
then
	clear
	echo "Installing Packages/Modules."
	pip3 install paho-mqtt >/dev/null
fi

clear
echo "Starting Web Server Now."
