#!/usr/bin/env  python
# -*- coding: utf-8 -*-
import argparse
import datetime
from Heizung.Heizung import *
import os
import time
import dateutil.parser
import Sensoren as sens

parser = argparse.ArgumentParser(description='HeizungLogger.')
parser.add_argument('--timestep',help='Time between to Logs in seconds',default=5)
parser.add_argument('--filename',help='last part of filename',default="HeizungLog")
parser.add_argument('--directory',help='directory to store data',default="~")

args = parser.parse_args()

myHeizung = Heizung('Z',withCrc=False)
mySensors = sens.Sensors()

if not(os.path.isdir(args.directory)):
  os.mkdir(args.directory)

sensIDListe = myHeizung.getTempSensors()[1] 
sensNamenListe = []
for n in sensIDListe:
  sensNamenListe.append(mySensors.sensors[n])
print sensNamenListe

heatm2 = 0
heatm1 = 0

while(1):
  filename = args.directory+'/'+str(datetime.datetime.now().date())+'_'+args.filename+'.log'
  print (filename )
  
  if not(os.path.isfile(filename)):
    fd = open(filename,"w")
    fd.write("Zeit;Uhrzeit;"+str(sensNamenListe)[1:-1].replace(',',';').replace('\'','').decode()+";Stufe1 [s];Stufe 2 [s]\r\n")
    fd.close()
  
  actualTime = datetime.datetime.now()
  timeString = str(actualTime.time().hour)+':'+str(actualTime.time().minute)+':'+str(actualTime.time().second)
  tListe = []
  for i in range(0,len(sensNamenListe)):
    tListe.append(  int(myHeizung.getTemperature(i)[1])/2.0  )
  print tListe
  res,heat1,heat2 = myHeizung.getHeater()
  if (heatm1 < 30) and (heatm1 > 0) and (heatm2 == 0) and (heat1 == 0):
  	 print("!!!!!!!!!!!!!!!!!!!!! Heater-Error !!!!!!!!!!!!!!!!!!!!!")
  
  heatm2 = heatm1
  heatm1 = heat1
  
  fd = open(filename,"a+")
  fd.write(actualTime.isoformat()+';'+timeString+';'+str(tListe)[1:-1].replace(',',';').replace(' ','') +';'+ str(heat1) +';'+ str(heat2)  +"\r\n")
  fd.close()
  time.sleep(int(args.timestep))
  