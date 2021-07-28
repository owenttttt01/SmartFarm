#!/usr/bin/env python3
# Code Cell 1.
# Import the dweepy module that is a collection of functions that make it  
# easier to communicate with dweet.io 
import dweepy

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
#GreenLEDPin =    #Add values: add the pin number for the green LED
# the PIN of the red LED
#RedLEDPin   =    #Add values: add the pin number for the red LED
#=============================================

# Setup the direction of the GPIO pins - either INput or OUTput 
# The PINs that connect LEDs must be set to OUTput mode:
GPIO.setup(GreenLEDPin, GPIO.OUT)
GPIO.setup(RedLEDPin, GPIO.OUT)
print()

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
        print()

    elif  lit1 == "g": #If the user chose the green LED
        print("Activate Green LED")
        GPIO.output(GreenLEDPin, True) # True = set 3.3V on the pin
        GPIO.output(RedLEDPin,   False) #False = set 0V on the pin
        print()

    elif  lit1 == "q": #If the user chose to quit the program
        print("Deactivate All LEDs")
        GPIO.output(GreenLEDPin, False) # True = set 3.3V on the pin
        GPIO.output(RedLEDPin,   False) #False = set 0V on the pin
        exit()

    else:  #If the user entered something other than r, g, or q.
        print("Please enter r for red, g for green, or q to quit.")
