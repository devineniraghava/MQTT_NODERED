#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 11:13:21 2022

@author: rdevinen
"""
import time
import paho.mqtt.client as mqtt    #import client library

# def on_connect(client, userdata, flags, rc):
#    if rc==0:
#       print("connected ok")
      
      
# broker = "localhost"      
# broker_address="test.mosquitto.org" #use external broker

# client = mqtt.Client("python1")             # create new instance 
# client.on_connect=on_connect  # bind call back function
# client.connect(broker) # connect to broker
# client.loop_start()  # Start loop 
# time.sleep(4) # Wait for connection setup to complete

# client.loop_stop()    # Stop loop 
# client.disconnect()







#%%

import paho.mqtt.client as mqtt #import the client1
import time
############
def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
########################################
# broker_address="localhost"
broker_address="test.mosquitto.org" #use external broker
broker_address= "192.168.50.1"  #Broker address

# broker_address="iot.eclipse.org"
print("creating new instance")
client = mqtt.Client("P1") #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address) #connect to broker
client.loop_start() #start the loop
print("Subscribing to topic","house/bulbs/bulb1")
client.subscribe("house/bulbs/bulb1")
print("Publishing message to topic","house/bulbs/bulb1")
client.publish("house/bulbs/bulb1","OFF")
time.sleep(4) # wait
client.loop_stop() #stop the loop

















#%%