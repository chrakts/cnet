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

class Clima(CNET):
  def __init__(self,node,comPort="", baudRate=57600, backChannel="TLog", withCrc = cnet_crc_constants_t.noCRC, timeout=3000):
    super(self.__class__,self).__init__(comPort , baudRate, backChannel, withCrc, timeout)
    self.node = node
    
  def getSerialNumber(self):
    return(self.sendCommand(self.node+"Ps"))
    
  def getIDNumber(self):
    return(self.sendCommand(self.node+"Pi"))

  def getIndex(self):
    return(self.sendCommand(self.node+"Px"))

  def setSecurityKey(self,key):
    return(self.sendCommand(self.node+"SK"+key)[0])

  def setSecurityKey(self,key):
    return(self.sendCommand(self.node+"SK"+key)[0])

  def getFreeMemory(self):
    boolAnswer,answer = self.sendCommand(self.node+"Sm")
    if boolAnswer==True:
      return(True,int(answer))
    else:
      return(False,-1)

  def makeReset(self):
    boolAnswer,answer = self.sendCommand(self.node+"SRReset")
    return boolAnswer
    
  def makeBootload(self):
    boolAnswer,answer = self.sendCommand(self.node+"SBBootload")
    return boolAnswer
  
  def getTemperature(self):
    (boolResult,Result) = self.sendCommand(self.node+"Ct")
    print(Result)
    try:
      fResult = float(Result)
      return(boolResult,fResult)
    except:    
      return(False,-999.9)
  	 
  def getHumidity(self):
    (boolResult,Result) = self.sendCommand(self.node+"Ch")
    print(Result)
    try:
      fResult = float(Result)
      return(boolResult,fResult)
    except:    
      return(False,-999.9)

  def getAbsoluteHumidity(self):
    (boolResult,Result) = self.sendCommand(self.node+"Ca")
    print(Result)
    try:
      fResult = float(Result)
      return(boolResult,fResult)
    except:    
      return(False,-999.9)
  	 
  def getDewPoint(self):
    (boolResult,Result) = self.sendCommand(self.node+"Cd")
    print(Result)
    try:
      fResult = float(Result)
      return(boolResult,fResult)
    except:    
      return(False,-999.9)
  	 
  def getPressure(self):
    (boolResult,Result) = self.sendCommand(self.node+"Cp")
    print(Result)
    try:
      fResult = float(Result)
      return(boolResult,fResult)
    except:    
      return(False,-999.9)
  	 
  def getSealevel(self):
    (boolResult,Result) = self.sendCommand(self.node+"Cs")
    print(Result)
    try:
      fResult = float(Result)
      return(boolResult,fResult)
    except:    
      return(False,-999.9)
  	 
  def getLight(self):
    (boolResult,Result) = self.sendCommand(self.node+"Cl")
    print(Result)
    try:
      fResult = float(Result)
      return(boolResult,fResult)
    except:    
      return(False,-999.9)
  	 
test = Clima('C',withCrc=True)
print( test.getTemperature() )
print( test.getHumidity() )
print( test.getAbsoluteHumidity() )
print( test.getDewPoint() )
print( test.getPressure() )
print( test.getSealevel() )
print( test.getLight() )

