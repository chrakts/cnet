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

class Heizung(CNET):
  def __init__(self,node='Z',comPort="", baudRate=38400, backChannel="HEIZUNG", withCrc = cnet_crc_constants_t.noCRC, timeout=5000):
    super(self.__class__,self).__init__(comPort, baudRate, backChannel, withCrc, timeout)
    self.node = node
    
  def getHeater(self):
    try:
      boolAnswer,answer = self.sendCommand(self.node+"H1")
      if boolAnswer == True:
        Heater1 = int(answer)
        boolAnswer,answer = self.sendCommand(self.node+"H2")
        if boolAnswer == True:
          Heater2 = int(answer)
          return(True,Heater1,Heater2)
        else:
          return(False,-1,-1)
      else:
        return(False,-1,-1)
    except:
      return(False,-1,-1)
      
  def getTempSensors(self):
    i=0
    notReady = True
    idList = list()
    while(notReady):
      boolAnswer,answer = self.sendCommand(self.node+"TS"+str(i))
      i += 1
      if boolAnswer == False:
        notReady = False
      try:
        int(answer,16)  # testet nur, ob tatsaechlich eine gueltige Seriennummer uebertragen wurde.
        idList.append(answer)
      except:
        notReady = False
    return(boolAnswer,idList)    

  def getTemperature(self,sensor):
    boolAnswer,answer = self.sendCommand(self.node+"TT"+str(sensor))
    return( boolAnswer,answer )  	
  	 
#test = Heizung('Z',withCrc=False)
#print( test.getTempSensors() )
#for i in range(0,4):
# print test.getTemperature(i)
#
#print( test.getHeater() )
