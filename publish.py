#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 15:27:13 2022

@author: rdevinen
"""

import paho.mqtt.client as mqtt #import the client1
# broker_address="localhost" 
broker_address="test.mosquitto.org" #use external broker
client = mqtt.Client("P1") #create new instance
client.connect(broker_address) #connect to broker
client.publish("house/main-light","OFF")#publish



#%%





















#%%