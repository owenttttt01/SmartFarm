#!/usr/bin/env python3

# Code Cell 1.
# Import the dweepy module that is a collection of functions that make it  
# easier to communicate with dweet.io 
import dweepy
import os

_=os.system("clear")

#Code cell 5

#===================
#myThing = "your_thing_name" #Add value: add your dweet thing name
===================

print('sending dweets #1...')
send_dweet = dweepy.dweet_for(myThing,{"dweet by": "Tom", "message" : "testing 123"}) #this function sends data to dweet.io
print('sending dweets #2...')
send_dweet = dweepy.dweet_for(myThing,{"dweet by": "Dick", "message" : "testing 456"}) 
print('sending dweets #3...')
send_dweet = dweepy.dweet_for(myThing,{"dweet by": "Harry", "message" : "testing 789"}) 
#print(send_dweet)
print()

print("getting latest dweet...")
latest_dweet = dweepy.get_latest_dweet_for(myThing) #get latest dweet
latest_created = latest_dweet[0]["created"]  #put the created value of the lastest dweet into a variable
latest_content = latest_dweet[0]["content"]  
print("Latest dweet time:", latest_created)
print("Latest dweet content:", latest_content)
print("Latest dweet JSON")
print(latest_dweet)
print()

print("getting all dweets...")
all_dweets = dweepy.get_dweets_for(myThing)
print(all_dweets)
print()

print("getting the last 3rd dweet specifically...")
specific_created = all_dweets[2]["created"]  #put the created value of the specific dweet into a variable
specific_content = all_dweets[2]["content"]  
print("Specific dweet time:", specific_created)
print("Specific dweet content:", specific_content)
print("Specific dweet JSON")
print(all_dweets[2])
print()


# Alternatively can send dweet via browser
# https://dweet.io/dweet/for/{my-thing-name}?text=mydweet
#
# Real time streaming
# curl -i https://dweet.io/listen/for/dweets/from/my-thing-name
# dweepy.listen_for_dweets_from('this_is_a_thing')
#
# Alert
# https://dweet.io/alert/{recipients}/when/{thing}/{condition}?key={key}
# dweepy.set_alert
# dweepy.get_alert('this_is_a_thing', 'this-is-a-key')
# 
# References
# https://dweet.io/
# https://github.com/paddycarey/dweepy/blob/master/README.rst
