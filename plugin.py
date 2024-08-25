import socket
import time
class Plugin:
  @classmethod
  def pluginInfo(cls):
    return {
      'description': 'set store values',
      'data': [
        {
        'path': '*',
        'description': 'test',
        }
      ]
    }
  def __init__(self,api):
    self.api=api
    self.counter=0
    self.host="localhost"
    self.port=9100
  def handleLine(self,line):
    self.api.debug("received: %s",line)
    nv=line.rstrip().split("=")
    if len(nv) != 2:
      return
    if self.api.addData(nv[0],nv[1]):
      self.counter+=1
    self.api.setStatus("NMEA" if self.counter > 0 else "RUNNING","%d records, %s:%d"%(self.counter,self.host,self.port))
  def run(self):
    self.api.log("storetest started %s:%d",self.host,self.port)
    sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((self.host, self.port))
    sock.settimeout(1)
    self.api.setStatus('RUNNING',"listening on %s:%d"%(self.host,self.port))
    buffer=""
    while not self.api.shouldStopMainThread():
      try:
        data = sock.recv(1024)
        if len(data) > 0:
          buffer=buffer+data.decode('ascii','ignore')
          lines=buffer.splitlines(True)
          if len(lines) > 0:
            num=len(lines)
            if lines[-1][-1]!='\n':
              num=num-1
            for i in range(num):
              self.handleLine(lines[i])
            if num != len(lines):
              buffer=lines[-1]
            else:
              buffer=""

        else:
          time.sleep(1)
      except socket.timeout:
        pass
