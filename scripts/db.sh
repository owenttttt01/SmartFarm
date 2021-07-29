clear
apt-get -y install python3-pip >/dev/null
clear
echo "Installation Status: 25% Complete"
pip3 install paho-mqtt >/dev/null
clear
echo "Installation Status: 50% Complete"
apt-get -y install curl >/dev/null
clear
echo "Installation Status: 75% Complete"
apt-get -y install expect >/dev/null
clear
echo "Installation Status: 100% Complete. Starting Web Server now."
