#!/usr/bin/env python3

# Code Cell 1.

# Import the dweepy module that is a collection of functions that make it  
# easier to communicate with dweet.io 
import dweepy

#===================
#myThing = "your_thing_name" #Add value: add your dweet thing name
#===================

# Import the GPIO modules to control the GPIO pins of the Raspberry Pi
# Uncomment the following only when testing on a physcial Rasberry Pi
# Comment the following when testing on a Raspbian VM
#import RPi.GPIO as GPIO

# Import the Mock GPIO modules to control the Mock GPIO pins of the Raspberry Pi
# Uncomment the following when testing on a Raspbian VM
# Comment the following when testing on a physcial Rasberry Pi
import EmulateGPIO as GPIO

# Import to clear cell output with code
from IPython.display import clear_output

# Import the time module to control the timing of your application (e.g. add delay, etc.)
import time

import os

_=os.system("clear")

# Code Cell 2.
#Setup hardware
# Set the desired pin numbering scheme:
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Create variables for the GPIO PINs the LEDs are connected to
# ============================================
# the PIN of the green LED
GreenLEDPin = 20   #Add values: add the pin number for the green LED
# the PIN of the red LED
RedLEDPin   = 21   #Add values: add the pin number for the red LED
#=============================================

# Setup the direction of the GPIO pins - either INput or OUTput 
# The PINs that connect LEDs must be set to OUTput mode:
GPIO.setup(GreenLEDPin, GPIO.OUT)
GPIO.setup(RedLEDPin, GPIO.OUT)
GPIO.output(GreenLEDPin, False) # True = set 3.3V on the pin
GPIO.output(RedLEDPin,   False) #False = set 0V on the pin
print('All LEDs are turned OFF' + '\n')

#Code Cell 4.
while True:
	# Asks the user to select the LED. Put the response into a variable.
	lit = input("Which LED should be lit? (r)ed or (g)reen? (q) to quit: ")

	# convert the input to lowercase and put it in another variable.
	lit1 = lit.lower()

	#Set the LED state based on the user input
	if lit1 == "r": #If the user chose the red LED
		print("Activate Red LED")
		GPIO.output(GreenLEDPin, False) # False = set 0V on the pin
		GPIO.output(RedLEDPin,   True)  # True = set 3.3V on the pin
		print('sending dweet...')
		old_dweet = dweepy.dweet_for(myThing, {"dweet": "Red"}) #this function sends data to dweet.io
		old_created = old_dweet['created'] #get the time stamp of the first dweet
		print('send dweet@' , old_created + '\n')
		break

	elif  lit1 == "g": #If the user chose the green LED
		print("Activate Green LED")
		GPIO.output(GreenLEDPin, True) # True = set 3.3V on the pin
		GPIO.output(RedLEDPin,   False) #False = set 0V on the pin
		print('sending dweet...')
		old_dweet = dweepy.dweet_for(myThing, {"dweet": "Green"}) #this function sends data to dweet.io
		old_created = old_dweet['created'] #get the time stamp of the first dweet
		print('send dweet@' , old_created + '\n')
		break

	elif  lit1 == "q": #If the user chose to quit the program
		GPIO.output(GreenLEDPin, False) # True = set 3.3V on the pin
		GPIO.output(RedLEDPin,   False) #False = set 0V on the pin
		print('Deavtivate All LEDs' + '\n')
		exit()

	else:  #If the user entered something other than r, g, or q.
		print("Please enter r for red, g for green, or q to quit.")

#Code cell 6.

counter = 0

while True:
	new_dweet = dweepy.get_latest_dweet_for(myThing) #get latest dweet
	new_created = new_dweet[0]["created"] #put the created value of the lastest dweet into a variable
	if new_created != old_created: #check to see if the the old dweet is different from the new dweet
		counter += 1
		print(str(counter) + " New dweet detected!",end='\n')
		old_created = new_created

		if lit1 == "g":
			print('receive new dweet@' , new_created)
			print("Activate Red LED")
			GPIO.output(GreenLEDPin, False) # False = set 0V on the pin
			GPIO.output(RedLEDPin,   True)  # True = set 3.3V on the pin
			lit1 = "r"
			print()

		elif lit1 == "r":
			print('receive new dweet@' , new_created)
			print("Activiate Green LED")
			GPIO.output(GreenLEDPin, True) 
			GPIO.output(RedLEDPin,   False)
			lit1 = "g"
			print()
	time.sleep(1)

