#!/usr/bin/env  python
# -*- coding: utf-8 -*-

import sys, os

path = os.getcwd() 
path0 = os.path.split(path)[0] # up one directory
sys.path.append(path0)
print(path0)
from CNET.CNET import CNET

from exlcm import cnet_command_t
from exlcm import cnet_answer_t
from exlcm import cnet_crc_constants_t
from exlcm import cnet_constants_t

FANOFF = '0'
FANON1 = '1'
FANON2 = '2'
FANAUTO= 'A'

class Badeklima(CNET):
  def __init__(self,node='B',comPort="", baudRate=38400, backChannel="BADEKLIMA", withCrc = cnet_crc_constants_t.noCRC, timeout=1000):
    super(self.__class__,self).__init__(comPort) #comPort, baudRate, backChannel, withCrc, timeout)
    self.node = node
    
  def setTemperature(self,T):
    strT = str(int(T*10.0))
    boolAnswer,answer = self.sendCommand(self.node+"PT"+strT)
    if answer == "SetTsoll":
      return True
    else:
      return False
     	 
  def setHystTemperature(self,dT):
    strdT = str(int(dT*10.0))
    boolAnswer,answer = self.sendCommand(self.node+"Pt"+strdT)
    if answer == "SetTHysterese":
      return True
    else:
      return False
     	 
  def setFeuchte1(self,data):
    strData = str(int(data*10.0))
    boolAnswer,answer = self.sendCommand(self.node+"PF"+strData)
    if answer == "SetL1":
      return True
    else:
      return False
     	 
  def setHystFeuchte1(self,data):
    strData = str(int(data*10.0))
    boolAnswer,answer = self.sendCommand(self.node+"Pf"+strData)
    if answer == "SetL1-Hysterese":
      return True
    else:
      return False
     	 
  def setFeuchte2(self,data):
    strData = str(int(data*10.0))
    boolAnswer,answer = self.sendCommand(self.node+"PE"+strData)
    if answer == "SetL2":
      return True
    else:
      return False
     	 
  def setHystFeuchte2(self,data):
    strData = str(int(data*10.0))
    boolAnswer,answer = self.sendCommand(self.node+"Pe"+strData)
    if answer == "SetL2-Hysterese":
      return True
    else:
      return False
     	 
  def setLuefterOff(self):
    return( self.sendCommand(self.node+"P0") )

  def setLuefterOn1(self):
    return( self.sendCommand(self.node+"P1") )
     	 
  def setLuefterOn2(self):
    return( self.sendCommand(self.node+"P2") )
     	 
  def setLuefterAuto(self):
    return( self.sendCommand(self.node+"PA") )
  
  def setLuefter(self,status):
    return( self.sendCommand(self.node+"P"+status) )
  
  def setHeizungOff(self):
    print("Achtung - ergibt immer Timeout, da Gerät keine Antwort vorsieht")
    return( self.sendCommand(self.node+"SC") )
  
  def setHeizungOn(self):
    print("Achtung - ergibt immer Timeout, da Gerät keine Antwort vorsieht")
    return( self.sendCommand(self.node+"SH") )
  
  def setHeizung(self,status):
    if status == 0:
      return( self.setHeizungOff() )
    else:
      return( self.setHeizungOn() )
      
  
  def getIstStatus(self):
    return( self.sendCommand(self.node+"GI") )
  
  def getSollStatus(self):
    return( self.sendCommand(self.node+"GS") )
  	 
test = Badeklima('B',withCrc=False)
#print( test.setLuefterOn1() )
#print( test.setLuefterOn2() )
#print( test.setHeizung(0) )
print( test.getIstStatus() )
print( test.getSollStatus() )

