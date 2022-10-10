#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 15:29:11 2022

@author: rdevinen
"""
import numpy as np
import time
import json
import datetime
import random
from pythermalcomfort.utilities import v_relative, clo_dynamic, running_mean_outdoor_temperature
from pythermalcomfort.models import set_tmp
from pythermalcomfort.models import pet_steady
from pythermalcomfort.models import pmv_ppd

def prRed(skk): print("\033[31;1;m {}\033[00m" .format(skk)) 
def prYellow(skk): print("\033[33;1;m {}\033[00m" .format(skk)) 
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))



#%%





#%%
import paho.mqtt.client as mqttClient
import time


def on_log(client, userdata, level, buf):
    print("log: "+buf)
  
def on_connect(client, userdata, flags, rc):
  
    if rc == 0:
  
        print("Connected to broker")
  
        global Connected                #Use global variable
        Connected = True                #Signal connection 
  
    else:
  
        print("Connection failed")
  
def on_message(client, userdata, message):
    global node_data
    node_data = message.payload.decode('utf-8')
    print(node_data)
    data = random.randint(0,100)
    client.publish("topic/pmv", data , 2 )
    time.sleep(0.1)
  
Connected = False   #global variable for the state of the connection



broker_address= "192.168.50.1"  #Broker address
  
# broker_address= "192.168.0.205"  #Broker address
# broker_address="test.mosquitto.org" #use external broker

port = 1883                         #Broker port
# user = "yourUser"                    #Connection username
# password = "yourPassword"            #Connection password
  
client = mqttClient.Client("Python")               #create new instance
# client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.on_message= on_message                      #attach function to callback
# client.on_log=on_log
  
client.connect(broker_address, port=port)          #connect to broker
  
client.loop_start()        #start the loop
  
while Connected != True:    #Wait for connection
    time.sleep(0.1)
  
client.subscribe("application/#")


# while True:
#     data = random.randint(0,100)
#     client.publish("topic/pmv", data , 2 )
#     time.sleep(0.1)
  

  
try:
    while True:
        time.sleep(1)
  
except KeyboardInterrupt:
    print("exiting")
    client.disconnect()
    client.loop_stop()









#%%