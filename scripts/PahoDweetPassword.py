#!/usr/bin/env python3
import ssl
import dweepy
import os
import time
import json
import paho.mqtt.client as mqtt

_=os.system("clear")

broker_address="172.19.0.12"
client = mqtt.Client("publisher")

myThing = "sussyfarm"

counter = 0

old_dweet = dweepy.get_latest_dweet_for(myThing)
old_created = old_dweet[0]['created']
print(old_created)

master_password= "poggers"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        global connected
        connected=True
    else:
        print("Failed to connect, return code %d\n", rc)

#client.tls_set(ca_certs='/root/iot_vol/scripts/cacert/ca.crt', certfile=None, keyfile='/root/iot_vol/scripts/cacert/ca.key', cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS, ciphers=None)
#connected=False
#client.username_pw_set(username="justin",password="itztimmy")
#client.on_connect = on_connect
#client.connect(broker_address)
#client.loop_start()
#while connected != True:
#    time.sleep(0.1)
#client.loop_stop()

while True:
    #mqttc=mqtt.Client()
    latest_dweet = dweepy.get_latest_dweet_for(myThing)
    new_created = latest_dweet[0]['created']
    latest_cont = latest_dweet[0]['content']
    sorted_content = sorted(latest_cont.items(), key = lambda kv:kv[0])
    password_tuple = sorted_content[0]
    ap, dweet_password = password_tuple
    if new_created != old_created and master_password == dweet_password:
        counter += 1
        print(str(counter) + " New Dweet Detected", end = "\n")
        old_created = new_created
        print(type(latest_dweet))
        print("Latest dweet: \n" + str(latest_dweet))
       
        latest_created = latest_dweet[0]["created"]
        print("\nTime of created dweet: " + str(latest_created))
    
        #latest_content = latest_dweet[0]["content"]
        junk, sensor = sorted_content[1]
        junk2, zvalue = sorted_content[2]
        print("\nContent of latest dweet: " + "sensor: " + str(sensor) + ", zvalue: " + str(zvalue))


        #sorted_content = sorted(latest_content.items(), key = lambda kv:kv[0])
        
        #print(sorted_content)
        #print(type(sorted_content))
        #password_tuple = sorted_content[0]
        #print(password_tuple)   
        #ap, dweet_password = password_tuple
        #print(ap)
        #print(dweet_password)

        str_created = json.dumps(latest_created)
        #str_content = json.dumps(latest_content)

        str_created_r = str_created.replace('"',"")

        #replace = '" {}'
        #for i in replace:
         #   str_content = str_content.replace(i,"")
        #str_content_r = str_content.replace(":",",")
        #str_content_test = str_content.split(",")

        #file_object = open('output.txt', 'a')
        #file_object.write(str_created_r + ",")
        #file_object.write(str_content + "\n")
        #file_object.close()
        #client.publish("farm", str_created_r + "," +str_content)
        #print("farm", str_created_r + "," + str_content)
        print("farm", str_created_r + ",sensor:" + str(sensor) + ",zvalue:" + str(zvalue))
        time.sleep(1)
        
        #paho_result.wait_for_publish()          
        #print(paho_result.wait_for_publish()) 
    else:
        time.sleep(1)
    time.sleep(10)
