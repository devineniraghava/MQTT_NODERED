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
from pythermalcomfort.utilities import v_relative, clo_dynamic, running_mean_outdoor_temperature
from pythermalcomfort.models import use_fans_heatwaves
from pythermalcomfort.models import set_tmp
from pythermalcomfort.models import pet_steady
from pythermalcomfort.models import pmv_ppd
from pythermalcomfort.models import pmv

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
    global pmv_ppd_iso, pet_steady_res, set_res
    
    
    global node_data
    # print("Message received: "  + str(message.payload))
    a = message.payload.decode()
    node_data = json.loads(message.payload.decode('utf-8'))
    if node_data["deviceName"] == "Node_3_Heltec_LoRa_HTU21_Globe_BH1750_Wind":
    
        tdb = node_data["object"]["temp_ds18b20"] # dry bulb air temperature
        tr = node_data["object"]["mrtReading"] # mean radiant temperature
        v = node_data["object"]["vel_wind"] # air speed measured by the sensor
        met = 1.4
        v_r = v_relative(v=v, met=met) # relative air speed
        rh = node_data["object"]["hum_htu21"] # relative humidity
        clo = 0.85
        
        
        clo_d = clo_dynamic(clo=clo, met=met)
        
        pmv_iso = pmv(tdb=tdb, tr=tr, vr=v_r, rh=rh, met=met, clo=clo_d, standard='ISO', units="SI")
        # pmv_ppd_iso = pmv_ppd(tdb = tdb, tr = tr, vr = v_r, rh = rh, met = met, clo = clo, standard="ISO", units="SI")
        
        pet_steady_res = pet_steady(tdb = tdb, tr = tr, v = v, rh = rh, 
                                    met = met, clo = clo, p_atm = 1013.25, 
                                    position=1, age=60, sex=1, weight=90, height=1.6, wme=0)
        
        set_res = set_tmp(tdb=tdb, tr = tr, v = v, rh = rh, met = met, 
                          clo = clo, wme=0, body_surface_area=1.8258, p_atm=101325, 
                          body_position='standing', units='SI', limit_inputs=True)
        
        heatwaves = use_fans_heatwaves(tdb = tdb, tr =tr, v = v, 
                                                rh = rh, met = met, clo = clo, 
                                                wme=0, body_surface_area=1.8258, 
                                                p_atm=101325, body_position='standing', 
                                                units='SI', max_skin_blood_flow=80)
        
        
        date_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print("Message recieved at: {}".format(date_time))
        prYellow("Predicted Mean Vote: {}".format(pmv_iso))
        prYellow("Physiological Equivalent Temperature: {}".format(pet_steady_res))
        prYellow("Standard Effective Temperature: {}".format(set_res))
        print(tdb, tr, v, v_r, rh)
        
        node_data["object"]["python_time"] = date_time
        node_data["object"]["pet_steady_res"] = pet_steady_res
        node_data["object"]["set_res"] = set_res
        node_data["object"]["pmv_iso"] = pmv_iso
        node_data["object"]["t_core"] = heatwaves["t_core"] # Core temperature, [°C]
        node_data["object"]["heat_strain"] = heatwaves["heat_strain"] # True if the model predict that the person may be experiencing heat strain
        node_data["object"]["heat_strain_blood_flow"] = heatwaves["heat_strain_blood_flow"] # True if heat strain is caused by skin blood flow (m_bl) reaching its maximum value
        node_data["object"]["heat_strain_w"] = heatwaves["heat_strain_w"] # True if heat strain is caused by skin wettedness (w) reaching its maximum value
        node_data["object"]["heat_strain_sweating"] = heatwaves["heat_strain_sweating"] # True if heat strain is caused by regulatory sweating (m_rsw) reaching its maximum value
        
        json_object = json.dumps(node_data, indent = 4) 
        # print(json_object)
        client.publish("topic/pmv", json_object , 2 )
    
    
    
    

  
Connected = False   #global variable for the state of the connection
  
broker_address= "192.168.50.1"  #Broker address
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


# while Connected != True:    #Wait for connection
#     time.sleep(0.1)
  
# client.publish("topic/pmv", "sample_PMV" )


  
try:
    while True:
        time.sleep(1)
  
except KeyboardInterrupt:
    print("exiting")
    client.disconnect()
    client.loop_stop()









#%%