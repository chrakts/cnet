#!/usr/bin/env  python
# -*- coding: utf-8 -*-
import argparse
import datetime
from Heizung.Heizung import *
import os
import time
import dateutil.parser
import Sensoren as sens
from inireader import reader
import smtplib
import email.utils
from email.mime.text import MIMEText
import getpass

def sendEmail(config,fr,to,sub,text):
  # Prompt the user for connection info
  to_email = config[to]['user']
  servername = config[fr]['server']
  username = config[fr]['user']
  password = config[fr]['pass']

  # Create the message
  msg = MIMEText(text)
  msg.set_unixfrom('author')
  msg['To'] = email.utils.formataddr(('Recipient', to_email))
  msg['From'] = email.utils.formataddr(('Heizung', 'zeug@cmja.de'))
  msg['Subject'] = sub

  server = smtplib.SMTP(servername)
  try:
      server.set_debuglevel(True)

      # identify ourselves, prompting server for supported features
      server.ehlo()

      # If we can encrypt this session, do it
      if server.has_extn('STARTTLS'):
          server.starttls()
          server.ehlo() # re-identify ourselves over TLS connection

      server.login(username, password)
      server.sendmail(username, [to_email], msg.as_string())
  finally:
      server.quit()


parser = argparse.ArgumentParser(description='HeizungLogger.')
parser.add_argument('--timestep',help='Time between to Logs in seconds',default=5)
parser.add_argument('--filename',help='last part of filename',default="HeizungLog")
parser.add_argument('--directory',help='directory to store data',default="~/cnetdata")

args = parser.parse_args()

myHeizung = Heizung('Z',withCrc=False)
mySensors = sens.Sensors()
EmailConfig = reader(os.path.expanduser("~/.myinfo.ini"))

directory = os.path.expanduser(args.directory)

if not(os.path.isdir(directory)):
  os.mkdir(directory)

sensIDListe = myHeizung.getTempSensors()[1] 
sensNamenListe = []
for n in sensIDListe:
  sensNamenListe.append(mySensors.sensors[n])
print(sensNamenListe)

heatm2 = 0
heatm1 = 0

while(1):
  filename = directory+'/'+str(datetime.datetime.now().date())+'_'+args.filename+'.log'
  print (filename )
  
  if not(os.path.isfile(filename)):
    fd = open(filename,"w")
    fd.write("Zeit;Uhrzeit;"+str(sensNamenListe)[1:-1].replace(',',';').replace('\'','')+";Stufe1 [s];Stufe 2 [s]\r\n")
    fd.close()
  
  actualTime = datetime.datetime.now()
  timeString = str(actualTime.time().hour)+':'+str(actualTime.time().minute)+':'+str(actualTime.time().second)
  tListe = []
  for i in range(0,len(sensNamenListe)):
    tListe.append(  int(myHeizung.getTemperature(i)[1])/2.0  )
  print (tListe)
  res,heat1,heat2 = myHeizung.getHeater()
  if (heatm1 < 30) and (heatm1 > 0) and (heatm2 == 0) and (heat1 == 0):
    print("!!!!!!!!!!!!!!!!!!!!! Heater-Error !!!!!!!!!!!!!!!!!!!!!")
    sendEmail(EmailConfig,'zeug','personal',"Fehler in der Heizung","Die Heizung hat einen Fehlerzustand")

  
  heatm2 = heatm1
  heatm1 = heat1
  
  fd = open(filename,"a+")
  fd.write(actualTime.isoformat()+';'+timeString+';'+str(tListe)[1:-1].replace(',',';').replace(' ','') +';'+ str(heat1) +';'+ str(heat2)  +"\r\n")
  fd.close()
  time.sleep(int(args.timestep))
  
