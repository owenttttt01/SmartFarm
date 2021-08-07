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
import paho.mqtt.publish as publish
from cryptography.fernet import Fernet
import hashlib
_=os.system("clear")

broker_address="172.19.0.12"

daylight_sensor = mqtt.Client("Daylight",clean_session=True)
moisture_sensor = mqtt.Client("Moisture")
thermometer = mqtt.Client("Temperature")
motion_sensor = mqtt.Client("Motion")

myThing = "sussyfarm"

counter = 0

old_dweet = dweepy.get_latest_dweet_for(myThing)
old_created = old_dweet[0]['created']
print(old_created)

#Dweet Password
master_password= "P@sswordC0$T"

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

def on_check(sensor_name, status):
    if sensor_name in sensor_array:
        position = sensor_array.index(sensor_name)
        if  (position == 0):
            device_id = "1"

            if (status == "on" or status == "ON"):
                sensor_dict["Smart Light"] = "ON"
                deviceStatus = "ON"
                GPIO.output(YellowLEDPin, True)
                os.system('curl http://172.19.0.13:8080/update/'+device_id+'?"DeviceStatus='+deviceStatus+'"')
            else:
                sensor_dict["Smart Light"] = "OFF"
                deviceStatus = "OFF"
                GPIO.output(YellowLEDPin, False)
                os.system('curl http://172.19.0.13:8080/update/'+device_id+'?"DeviceStatus='+deviceStatus+'"')

        elif (position == 1):
            device_id = "2"

            if (status == "on" or status == "ON"):
                sensor_dict["Smart Sprinkler"] = "ON"
                deviceStatus = "ON"
                GPIO.output(BlueLEDPin, True)
                os.system('curl http://172.19.0.13:8080/update/'+device_id+'?"DeviceStatus='+deviceStatus+'"')
            else:
                sensor_dict["Smart Sprinkler"] = "OFF"
                deviceStatus = "OFF"
                GPIO.output(BlueLEDPin, False)
                os.system('curl http://172.19.0.13:8080/update/'+device_id+'?"DeviceStatus='+deviceStatus+'"')

        elif (position == 2):
            device_id = "3"
            device_did = "1"

            if (status == "on" or status == "ON"):
                sensor_dict["Smart Shelter"] = "ON"
                sensor_dict["Smart Light"] = "ON"
                deviceStatus = "ON"
                GPIO.output(GreenLEDPin, True)
                GPIO.output(YellowLEDPin, True)
                os.system('curl http://172.19.0.13:8080/update/'+device_id+'?"DeviceStatus='+deviceStatus+'"')
                os.system('curl http://172.19.0.13:8080/update/'+device_did+'?"DeviceStatus='+deviceStatus+'"')
            else:
                sensor_dict["Smart Shelter"] = "OFF"
                deviceStatus = "OFF"
                GPIO.output(GreenLEDPin, False)
                os.system('curl http://172.19.0.13:8080/update/'+device_id+'?"DeviceStatus='+deviceStatus+'"')

        elif (position == 3):
            device_id = "4"

            if (status == "on" or status == "ON"):
                sensor_dict["Smart Scarecrow"] = "ON"
                deviceStatus = "ON"
                GPIO.output(RedLEDPin, True)
                os.system('curl http://172.19.0.13:8080/update/'+device_id+'?"DeviceStatus='+deviceStatus+'"')
            else:
                sensor_dict["Smart Scarecrow"] = "OFF"
                deviceStatus = "OFF"
                GPIO.output(RedLEDPin, False)
                os.system('curl http://172.19.0.13:8080/update/'+device_id+'?"DeviceStatus='+deviceStatus+'"')
        

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
              sensor_dict["Smart Light"] = "ON"
              deviceStatus = "ON"
              GPIO.output(GreenLEDPin, True)
              GPIO.output(YellowLEDPin,True)
          else:
              sensor_dict["Smart Shelter"] = "OFF"
              deviceStatus = "OFF"
              GPIO.output(GreenLEDPin, False)

      elif (position == 3):
          device_name = "SmartScarecrow"
          measuring_factor = "Motion"
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

      return measuring_factor

  else:
        data = "invalid"
        print("Invalid Data")

        return data

print("\nAll Smart Devices are currently OFF\n")
GPIO.output(GreenLEDPin, False)
GPIO.output(RedLEDPin, False)
GPIO.output(YellowLEDPin, False)
GPIO.output(BlueLEDPin, False)

#print(GPIO.gpio_function(GreenLEDPin))
#print(GPIO.gpio_function(RedLEDPin))
#print(GPIO.gpio_function(YellowLEDPin))
#print(GPIO.gpio_function(BlueLEDPin))
connected=False

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        global connected
        connected=True
    else:
        print("Failed to connect, return code %d\n", rc)


while True:
    #mqttc=mqtt.Client()
    latest_dweet = dweepy.get_latest_dweet_for(myThing)
    new_created = latest_dweet[0]['created']
    latest_cont = latest_dweet[0]['content']
    sorted_content = sorted(latest_cont.items(), key = lambda kv:kv[0])
    password_tuple = sorted_content[0]
    ap, dweet_password = password_tuple
    if new_created != old_created and master_password == dweet_password:
        data = "valid"
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
         
        checkvalue = isinstance(zvalue, int)
        status = "null"
        if zvalue == "on" or zvalue == "off" or zvalue == "ON" or zvalue == "OFF":
            on_check(sensor, zvalue)
            measuring_factor = "invalid"
            status = "sent"
        elif checkvalue == False:
            print("Invalid Data")
            notString = "False"
            measuring_factor = "invalid"
        elif checkvalue == True:
            print("Valid Data")
            measuring_factor = sensor_check(sensor, zvalue)
            notString = "True"


        print("\nCurrent LED Status")
        print("===========================================")
        print("Smart Light (Yellow LED): " + sensor_dict["Smart Light"])
        print("Smart Sprinkler" + B+"(Blue LED): " + W+ sensor_dict["Smart Sprinkler"])
        print("Smart Shelter " + G+"(Green LED): " + W+ sensor_dict["Smart Shelter"])
        print("Smart Scarecrow "+ R+"(Red LED): " + W+ sensor_dict["Smart Scarecrow"])
        print("===========================================")

        str_created = json.dumps(latest_created)

        str_created_r = str_created.replace('"',"")
        
        
        if measuring_factor != "invalid" and notString == "True":
            if measuring_factor == "Light_Intensity":
                 
                #cipher_key = Fernet.generate_key()
                #cipher = Fernet(cipher_key)

                #writing key into a file
                #keyfile = open("cipher_key", "wb")
                #keyfile.write(cipher_key)
                #keyfile.close()

                keyfile = open("cipher_key", "rb")
                cipher = Fernet(keyfile.readline())
                keyfile.close()

                daylight_sensor.tls_set(ca_certs='/root/iot_vol/SmartFarm/scripts/cacert/ca.crt', tls_version=ssl.PROTOCOL_TLS)

                daylight_sensor.username_pw_set(username="Daylight",password="Passw0rd$")
                daylight_sensor.on_connect = on_connect
                daylight_sensor.connect(broker_address)
                
                daylight_sensor.loop_start()
                while connected != True:
                    time.sleep(0.1)
                daylight_sensor.loop_stop()
                message = str_created_r + ",sensor:" + str(sensor) + ",zvalue:"+ str(zvalue)
                encrypted_message = cipher.encrypt(message.encode())
                
                #turn encrypted msg into a string
                out_message = encrypted_message.decode()
                daylight_sensor.publish('farm/'+measuring_factor, out_message, qos=1)
                
                print("\nInformation Sent Across:\n", str_created_r + ",sensor:" + str(sensor) + ",zvalue:" + str(zvalue))
                message_hash = hashlib.md5(encrypted_message).hexdigest()
                print("Hash of message sent: " + message_hash)
                print("Sent to topic: farm/"+measuring_factor)
                time.sleep(1)
                daylight_sensor.disconnect()
                print("Disconnected from MQTT Broker.")
                connected = False
                daylight_sensor.reinitialise()
            elif measuring_factor == "Soil_Moisture": 

                #cipher_key = Fernet.generate_key()
                #cipher = Fernet(cipher_key)

                #writing key into a file
                #keyfile = open("cipher_key", "wb")
                #keyfile.write(cipher_key)
                #keyfile.close()
                
                keyfile = open("cipher_key", "rb")
                cipher = Fernet(keyfile.readline())
                keyfile.close()
                
                moisture_sensor.tls_set(ca_certs='/root/iot_vol/SmartFarm/scripts/cacert/ca.crt', tls_version=ssl.PROTOCOL_TLS)
                connected=False
                moisture_sensor.username_pw_set(username="Moisture",password="Passw0rd$")
                moisture_sensor.on_connect = on_connect
                moisture_sensor.connect(broker_address)
                
                moisture_sensor.loop_start()
                while connected != True:
                    time.sleep(0.1)
                moisture_sensor.loop_stop()
                
                message = str_created_r + ",sensor:" + str(sensor) + ",zvalue:"+ str(zvalue)
                encrypted_message = cipher.encrypt(message.encode())
                
                #turn encrypted msg into a string
                out_message = encrypted_message.decode()
                moisture_sensor.publish('farm/'+measuring_factor, out_message)

                print("\nInformation Sent Across:\n", str_created_r + ",sensor:" + str(sensor) + ",zvalue:" + str(zvalue))
                message_hash = hashlib.md5(encrypted_message).hexdigest()
                print("Hash of message sent: " + message_hash)
                print("Sent to topic: farm/"+measuring_factor)
                time.sleep(1)
                moisture_sensor.disconnect()
                connected = False
                moisture_sensor.reinitialise()
                print("Disconnected from MQTT Broker.")
            elif measuring_factor == "Temperature":
                
                #cipher_key = Fernet.generate_key()
                #cipher = Fernet(cipher_key)

                #writing key into a file
                #keyfile = open("cipher_key", "wb")
                #keyfile.write(cipher_key)
                #keyfile.close()
                
                keyfile = open("cipher_key", "rb" )
                cipher = Fernet(keyfile.readline())
                keyfile.close()
                
                thermometer.tls_set(ca_certs='/root/iot_vol/SmartFarm/scripts/cacert/ca.crt', tls_version=ssl.PROTOCOL_TLS)
                thermometer.username_pw_set(username="Temperature",password="Passw0rd$")
                thermometer.on_connect = on_connect
                
                thermometer.connect(broker_address)
                thermometer.loop_start()
                while connected != True:
                    time.sleep(0.1)
                thermometer.loop_stop()
                
                message = str_created_r + ",sensor:" + str(sensor) + ",zvalue:"+ str(zvalue)
                encrypted_message = cipher.encrypt(message.encode())
                
                #turn encrypted msg into a string
                out_message = encrypted_message.decode()
                thermometer.publish('farm/'+measuring_factor, out_message)
                
                print("\nInformation Sent Across:\n", str_created_r + ",sensor:" + str(sensor) + ",zvalue:" + str(zvalue))
                message_hash = hashlib.md5(encrypted_message).hexdigest()
                print("Hash of message sent: " + message_hash)
                print("Sent to topic: farm/"+measuring_factor)
                time.sleep(1)
                thermometer.disconnect()
                
                connected = False  
                thermometer.reinitialise()
                print("Disconnected from MQTT Broker.")
            elif measuring_factor =="Motion": 

                #cipher_key = Fernet.generate_key()
                #cipher = Fernet(cipher_key)

                #writing key into a file
                #keyfile = open("cipher_key", "wb")
                #keyfile.write(cipher_key)
                #keyfile.close()
                
                keyfile = open("cypher_key", "rb")
                cipher = Fernet(keyfile.readline())
                keyfile.close()

                motion_sensor.tls_set(ca_certs='/root/iot_vol/SmartFarm/scripts/cacert/ca.crt', tls_version=ssl.PROTOCOL_TLS)
                motion_sensor.username_pw_set(username="Motion",password="Passw0rd$")
                motion_sensor.on_connect = on_connect
                motion_sensor.connect(broker_address)
                
                motion_sensor.loop_start()
                while connected != True:
                    time.sleep(0.1)
                motion_sensor.loop_stop()

                message = str_created_r + ",sensor:" + str(sensor) + ",zvalue:"+ str(zvalue)
                encrypted_message = cipher.encrypt(message.encode())
                #turn encrypted msg into a string
                out_message = encrypted_message.decode()
                motion_sensor.publish('farm/'+measuring_factor, out_message)
                
                print("\nInformation Sent Across:\n", str_created_r + ",sensor:" + str(sensor) + ",zvalue:" + str(zvalue))
                message_hash = hashlib.md5(encrypted_message).hexdigest()
                print("Hash of message sent: " + message_hash)
                print("Sent to topic: farm/"+measuring_factor)
                time.sleep(1)
                motion_sensor.disconnect()
                connected = False
                motion_sensor.reinitialise()
                print("Disconnected from MQTT Broker.")
                
        elif status == "sent":
            print("Data sent")
        else:
            print("No data sent")
            continue

        time.sleep(1)
        
    else:
        time.sleep(1)
    time.sleep(10)
