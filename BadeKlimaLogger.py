#!/usr/bin/env  python
# -*- coding: utf-8 -*-
import argparse
import datetime
from Badeklima.Badeklima import *
import os
import time
import dateutil.parser
import sys

parser = argparse.ArgumentParser(description='BadeKlima-Logger.')
parser.add_argument('--timestep',help='Time between to Logs in seconds',default=5)
parser.add_argument('--filename',help='last part of filename',default="BadeKlimaLog")
parser.add_argument('--directory',help='directory to store data',default="~")

args = parser.parse_args()

myBadeklima = Badeklima('B',withCrc=False,backChannel="MyBadeklima")

if not(os.path.isdir(args.directory)):
  os.mkdir(args.directory)

while(1):
  filename = args.directory+'/'+str(datetime.datetime.now().date())+'_'+args.filename+'.log'
  print (filename )
  
  if not(os.path.isfile(filename)):
    fd = open(filename,"w")
    fd.write("Zeit;Uhrzeit;Tist [°C];Hist [%];H [1]; V [1]; Tsoll [°C]; TH [K]; L1 [%]; LH1 [%]; L2 [%]; LH2 [%]; LS [1]\r\n")
    fd.close()
    
  actualTime = datetime.datetime.now()
  #Ist:   T=21.7, H=76.6, Li=2, H=1, V=1.
  #Soll:  T=25.4, TH=1.0, L1=75.2, L1H=2.6, L2=77.0, L2H=3.0, LS=0.
  timeString = "%02d:%02d:%02d"%(actualTime.time().hour,actualTime.time().minute,actualTime.time().second)
  resultIst,IstStrings = myBadeklima.getIstStatus()
  if resultIst:
    IstStrings = IstStrings.split(',')
    i=0
    istFloat=[]
    for ist in IstStrings:
      istFloat.append( float(ist.split('=')[1]) )
      i=i+1
    resultSoll,SollStrings = myBadeklima.getSollStatus()
    if resultSoll:
      SollStrings = SollStrings.split(',')
      i=0
      sollFloat=[]
      for soll in SollStrings:
        sollFloat.append( float(soll.split('=')[1]) )
        i=i+1
  
  if( resultIst and resultSoll ):
    fd = open(filename,"a+")
    fd.write(actualTime.isoformat()+';'+timeString)
    for ist in istFloat:
      fd.write(";"+str(ist))
    for soll in sollFloat:
      fd.write(";"+str(soll))
    fd.write("\r\n")
    fd.close()
  time.sleep(int(args.timestep))
