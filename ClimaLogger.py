#!/usr/bin/env  python
# -*- coding: utf-8 -*-
import argparse
import datetime
from Clima.Clima import *
import os
import time
import dateutil.parser
import sys

#sys.stdout = open('ClimaAusgabeLogger.log', 'w')
parser = argparse.ArgumentParser(description='ClimaLogger.')
parser.add_argument('--timestep',help='Time between to Logs in seconds',default=5)
parser.add_argument('--filename',help='last part of filename',default="ClimaLog")
parser.add_argument('--directory',help='directory to store data',default="~")

args = parser.parse_args()

myClima = Clima('C',withCrc=False,backChannel="MyClima")

if not(os.path.isdir(args.directory)):
	os.mkdir(args.directory)



while(1):
  filename = args.directory+'/'+str(datetime.datetime.now().date())+'_'+args.filename+'.log'
  print (filename )
  
  if not(os.path.isfile(filename)):
  	fd = open(filename,"w")
  	fd.write("Zeit;Uhrzeit;Temperatur [°C];rel. Feuchte [%];abs. Feuchte [g/m3]; Taupunkt [°C]; Luftdruck [mbar]; Licht [1]\r\n")
  	fd.close()
  
  actualTime = datetime.datetime.now()
  timeString = str(actualTime.time().hour)+':'+str(actualTime.time().minute)+':'+str(actualTime.time().second)
  temperature = myClima.getTemperature()
  humidity =    myClima.getHumidity()
  absHumidity = myClima.getAbsoluteHumidity()
  dewPoint =    myClima.getDewPoint()
  pressure = 	 myClima.getPressure()      
  light =       myClima.getLight()
  if(temperature[0] and humidity[0] and absHumidity[0] and dewPoint[0] and pressure[0] and light[0]):
    fd = open(filename,"a+")
    fd.write(actualTime.isoformat()+';'+timeString+';'+str(temperature[1]) +';'+  str(humidity[1]) +';'+ str(absHumidity[1]) +';'+ str(dewPoint[1]) +';'+ str(pressure[1]) +';'+ str(light[1])+"\r\n")
    fd.close()
  time.sleep(int(args.timestep))