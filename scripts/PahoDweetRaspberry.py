#!/usr/bin/env python3

# Import the GPIO modules to control the GPIO pins of the Raspberry Pi
# Uncomment the following only when testing on a physcial Rasberry Pi
# Comment the following when testing on a Raspbian VM
#import RPi.GPIO as GPIO

# Import the Mock GPIO modules to control the Mock GPIO pins of the Raspberry Pi
# Uncomment the following when testing on a Raspbian VM
# Comment the following when testing on a physcial Rasberry Pi
import EmulateGPIO as GPIO
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

#Dweet Password
master_password= "poggers"

#Emulate Raspberry Pi
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Lights
GreenLEDPin   = 20
RedLEDPin   = 21
BlueLEDPin   = 22
YellowLEDPin   = 23

GPIO.setup(GreenLEDPin, GPIO.OUT)
GPIO.setup(RedLEDPin, GPIO.OUT)
GPIO.setup(BlueLEDPin, GPIO.OUT)
GPIO.setup(YellowLEDPin, GPIO.OUT)

#Text Colour
R  = '\033[31m' # red
G  = '\033[32m' # green
B  = '\033[34m' # blue
W  = '\033[0m'  # white (normal)

sensor_array = ['Daylight','Moisture','Thermometer','Motion']

sensor_dict = {
        "Smart Light":"OFF",
        "Smart Sprinkler":"OFF",
        "Smart Shelter":"OFF",
        "Smart Scarecrow":"OFF",
        }

deviceStatus = "OFF"

def sensor_check(sensor_name, measuring_value):
  if sensor_name in sensor_array:
      position = sensor_array.index(sensor_name)
      #print(position)
      if  (position == 0):
          device_name = "SmartLight"
          measuring_factor = "Light_Intensity"
          device_id = "1"
          if (measuring_value < 60):
              sensor_dict["Smart Light"] = "ON"
              deviceStatus = "ON"
              GPIO.output(YellowLEDPin, True)
          else:
              sensor_dict["Smart Light"] = "OFF"
              deviceStatus = "OFF"
              GPIO.output(YellowLEDPin, False)

      elif (position == 1):
          device_name = "SmartSprinkler"
          measuring_factor = "Soil_Moisture"
          device_id = "2"
          if (measuring_value < 30):
              sensor_dict["Smart Sprinkler"] = "ON"
              deviceStatus = "ON"
              GPIO.output(BlueLEDPin, True)
          else:
              sensor_dict["Smart Sprinkler"] = "OFF"
              deviceStatus = "OFF"
              GPIO.output(BlueLEDPin, False)

      elif (position == 2):
          device_name = "SmartShelter"
          measuring_factor = "Temperature"
          device_id = "3"
          if (measuring_value > 35):
              sensor_dict["Smart Shelter"] = "ON"
              deviceStatus = "ON"
              GPIO.output(RedLEDPin, True)
          else:
              sensor_dict["Smart Shelter"] = "OFF"
              deviceStatus = "OFF"
              GPIO.output(RedLEDPin, False)

      elif (position == 3):
          device_name = "SmartScarecrow"
          measuring_factor = "Motion_Detection"
          device_id = "4"
          if (measuring_value > 35):
              sensor_dict["Smart Scarecrow"] = "ON"
              deviceStatus = "ON"
              GPIO.output(RedLEDPin, True)
          else:
              sensor_dict["Smart Scarecrow"] = "OFF"
              deviceStatus = "OFF"
              GPIO.output(RedLEDPin, False)

      print('\nDevice Status = '+deviceStatus)
      print('\nDevice Name = '+device_name)
      print('\nMeasuring factor = '+measuring_factor)
  else:
      print("Sensor name not recognised")


print("\nAll Smart Devices are currently OFF\n")
GPIO.output(GreenLEDPin, False)
GPIO.output(RedLEDPin, False)
GPIO.output(YellowLEDPin, False)
GPIO.output(BlueLEDPin, False)

#print(GPIO.gpio_function(GreenLEDPin))
#print(GPIO.gpio_function(RedLEDPin))
#print(GPIO.gpio_function(YellowLEDPin))
#print(GPIO.gpio_function(BlueLEDPin))


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        global connected
        connected=True
    else:
        print("Failed to connect, return code %d\n", rc)

client.tls_set(ca_certs='/root/iot_vol/SmartFarm/scripts/cacert/ca.crt', tls_version=ssl.PROTOCOL_TLS)
connected=False
client.username_pw_set(username="justin",password="itztimmy")
client.on_connect = on_connect
client.connect(broker_address)
client.loop_start()
while connected != True:
    time.sleep(0.1)
client.loop_stop()

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
        #print(type(latest_dweet))
        print("Latest dweet: \n" + str(latest_dweet))
       
        latest_created = latest_dweet[0]["created"]
        print("\nTime of created dweet: " + str(latest_created))
    
        junk, sensor = sorted_content[1]
        junk2, zvalue = sorted_content[2]
        print("\nContent of latest dweet: " + "sensor: " + str(sensor) + ", zvalue: " + str(zvalue))
        
        sensor_check(sensor, zvalue)
        print("\nCurrent LED Status")
        print("===========================================")
        print("Smart Light (Yellow LED): " + sensor_dict["Smart Light"])
        print("Smart Sprinkler" + B+"(Blue LED): " + W+ sensor_dict["Smart Sprinkler"])
        print("Smart Shelter " + G+"(Green LED): " + W+ sensor_dict["Smart Shelter"])
        print("Smart Scarecrow "+ R+"(Red LED): " + W+ sensor_dict["Smart Scarecrow"])
        print("===========================================")

        str_created = json.dumps(latest_created)

        str_created_r = str_created.replace('"',"")

        client.publish("farm", str_created_r + ",sensor:" + str(sensor) + ",zvalue:" + str(zvalue))
        print("\nInformation Sent Across:\n", str_created_r + ",sensor:" + str(sensor) + ",zvalue:" + str(zvalue))
        time.sleep(1)
        
    else:
        time.sleep(1)
    time.sleep(10)
