import time
from PyCRC.CRCCCITT import CRCCCITT
import lcm
from exlcm import cnet_command_t
from exlcm import cnet_answer_t
from exlcm import cnet_crc_constants_t
from exlcm import cnet_constants_t
import argparse
import serial

class CNET(object):
   def __init__(self,comPort="", baudRate=57600, backChannel="Klima", withCrc = cnet_crc_constants_t.noCRC, timeout=1000):
      if comPort != "":
         self.interface = serial.Serial(comPort, 57600, timeout=3)
      else:
         self.interface = backChannel
         self.lc = lcm.LCM("udpm://239.255.76.67:7667?ttl=1")
      if withCrc==True:
         self.crc = cnet_crc_constants_t.CRC_xmodem
      else:
         self.crc = cnet_crc_constants_t.noCRC
      self.crc = withCrc
      self.backChannel = backChannel
      self.timeout = timeout
      self.gotAnswer = False
      self.subscription = None
   
   def sendCommand(self,command):
      if type(self.interface)==str:
         boolAnswer,answer = self.sendCommandServer(command)
      else:
         boolAnswer,answer = self.sendCommandTTY(command)
      return(boolAnswer,answer)
            
   def sendCommandServer(self,command):
      self.msg = cnet_command_t()
      self.msg.command = command
      self.msg.target = self.backChannel
      self.msg.expect_answer = True
      self.msg.crcType = self.crc
      self.msg.timeout_ms = int(self.timeout)
      self.lc.publish("CNET", self.msg.encode())
      self.subscripe()
      if(self.msganswer.answer[-1]!='.'):
        return(False,self.msganswer.answer[:-1])
      else:
        return(True,self.msganswer.answer[:-1])
 #       return(self.msganswer.error,self.msganswer.answer[:-1])
        
      
   def sendCommandTTY(self,command):
      crcstring =  ("%04x" % (CRCCCITT().calculate(command)))  # ************************
      if self.crc != cnet_crc_constants_t.noCRC:
         self.outputTTY("\\>"+command+"<"+crcstring+"\\")
      else:
         self.outputTTY("\\>"+command+"<\\")
      result,resultBool,resultCRC,inTime = self.input()
      return(resultBool,result)
          
   def outputTTY(self,text):
      towrite = text
      self.interface.write(towrite.encode('ascii'))
        
   def _readline(self):
      eol = b'>'
      leneol = len(eol)
      line = bytearray()
      while True:
         c =  self.interface.read(1)
         if c:
            line += c
            if line[-leneol:] == eol:
               break
         else:
            break
      return bytes(line)
     
     
   def input(self):
      inTime = True
      hello = self._readline().decode('utf-8')
      if len(hello) == 0:
         return("",False,False,False)
      crcState = True
      crcString = ""
      if hello[0] != '<':
         print("!! start character error")
      if hello[-1] != '>':
         print("!! end character error")
      if self.crc != cnet_crc_constants_t.noCRC:
         crcString = hello[-5:-1]
         signString = hello[-6:-5]
         answerString = hello[1:-5]
         if crcString == ("%04x" % (CRCCCITT().calculate(answerString))):
            crcState = True
         else:
            crcState = False
            print("!! CRC error")
         answerString = answerString[0:-1] # das sign abtrennen
      else:
         answerString = hello[1:-2]
         signString = hello[-2:-1]
      if signString == '.':
         return(answerString,True,crcState,inTime)
      elif signString == '!':
         return(answerString,False,crcState,inTime)
      else:
         print("!! sign character error")
         return(answerString,False,crcState,inTime)

   def answer_handler(self,channel,data):
      self.msganswer = cnet_answer_t.decode(data)
      self.gotAnswer = True
      
   def subscripe(self):
      self.gotAnswer = False
      self.subscription = self.lc.subscribe(self.backChannel,self.answer_handler)
      try:
         while not self.gotAnswer:
            self.lc.handle()
      except KeyboardInterrupt:
         pass   
      if(self.msganswer.error==0):
         pass    # print("Antwort lautet:" + self.msganswer.answer)
      else:
         print("Timeout mit Antwort:" + self.msganswer.answer)
   def close(self):
      if type(self.interface)!=str:
         self.interface.close()

