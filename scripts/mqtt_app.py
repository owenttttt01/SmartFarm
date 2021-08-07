#!/usr/bin/env python3
import ssl
import os
import time
import paho.mqtt.client as mqtt
import re
import os
_=os.system("clear")

broker = "172.19.0.12"
client = mqtt.Client("subscriber")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        global connected
        connected=True
    else:
        print("Failed to connect, return code %d\n", rc)

def on_message(client, userdata, message):
    Messagereceived=True
    #read from keyfile
    keyfile = open("cipher_key", "rb")
    cipher = Fernet(keyfile.readline())
    keyfile.close()

    #print("received message = " + str(message.payload.decode("utf-8")))
    #print("message topic = " + str(message.topic))
    #check message hash
    message_hash = hashlib.md5(message.payload).hexdigest()
    print("Encrypted Message: " + message.payload.decode("utf-8"))
    print("Encrypted message hash: " + message_hash)
    #decrypt message)
    decrypted_message = cipher.decrypt(message.payload)

    sensor_msg = str(decrypted_message.decode("utf-8"))
    print("Sensor Message:" + sensor_msg)
    print("Topic received from: " + str(message.topic))

    #filter by timestamp, measuring factor and sensor name
    split_msg = sensor_msg.split(",")
    split_msg_sorted = sorted(split_msg)
    print(split_msg_sorted)
    #fixing up timestamp
    splitByReplace = split_msg_sorted[0].replace("T", " ")

    timestamp = re.sub('\.\d\d\dZ','', splitByReplace)
    timestamp2 = my_string = re.sub(r'(\d)\s+(\d)', r'\1\2', timestamp)
    timestamp2 = timestamp2[:10] + '%20' + timestamp2[10:]
    measuring_value = int(split_msg_sorted[2].split(":")[1])
    sensor_name = split_msg_sorted[1].split(":")[1]

    print("\nFiltered message = " + str(split_msg))
    print("\nTimestamp = " + str(timestamp2))
    print("\nSensor name = " + str(sensor_name))

    #check sensor name
    sensor_array = ['Daylight','Moisture','Thermometer','Motion']
    
    deviceStatus = "OFF" 
    if sensor_name in sensor_array:
        position = sensor_array.index(sensor_name)
        print(position)
        if  (position == 0):
            device_name = "SmartLight"
            measuring_factor = "Light_Intensity"
            device_id = "1"
            if (measuring_value < 60):
                deviceStatus = "ON"
        elif (position == 1):
            device_name = "SmartSprinkler"
            measuring_factor = "Soil_Moisture"
            device_id = "2"
            if (measuring_value < 30):
                deviceStatus = "ON"
        elif (position == 2):
            device_name = "SmartShelter"
            measuring_factor = "Temperature"
            device_id = "3"
            if (measuring_value > 35):
                deviceStatus = "ON"
        elif (position == 3):
            device_name = "SmartScarecrow"
            measuring_factor = "Motion_Detection"
            device_id = "4"
            if (measuring_value > 35):
                deviceStatus = "ON"
        
        print('\nDevice Status = '+deviceStatus)
        print('\nDevice Name = '+device_name)
        print('\nMeasuring factor = '+measuring_factor)
        
        #curling into database
        os.system('curl http://172.19.0.13:8080/add/'+device_name+'?"DeviceTime='+timestamp2+'&DeviceStatus='+deviceStatus+'&DeviceInformation='+measuring_factor+'%20level%20:%20'+str(measuring_value)+'"')
        os.system('curl http://172.19.0.13:8080/update/'+device_id+'?"DeviceStatus='+deviceStatus+'"')
        #os.system('curl http://172.19.0.13:8080/update/'+device_id+'?"DeviceTime='+timestamp2+'&DeviceStatus='+deviceStatus+'&DeviceInformation='+measuring_factor+'%20level%20:%20'+str(measuring_value)+'"')
        if device_id == "3" and deviceStatus == "ON":
            os.system('curl http://172.19.0.13:8080/update/1?"DeviceStatus=ON"')
    else:
        print("Sensor name not recognised")


    

Messagereceived=False

client.tls_set(ca_certs='/root/iot_vol/SmartFarm/scripts/cacert/ca.crt', tls_version=ssl.PROTOCOL_TLS)

connected=False
client.username_pw_set(username="Database",password="Passw0rd$")
client.on_message = on_message
client.connect(broker)
client.on_connect = on_connect
client.subscribe("farm/+")
client.loop_start()
while connected != True:
    time.sleep(0.1)

while Messagereceived != True:
    time.sleep(0.1)
client.loop_stop()

