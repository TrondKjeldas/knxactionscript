from serial import Serial
from time import sleep

class SerialAction:

    def __init__(self, name, port, speed, cmd):
        self.name = name
        self.port = port
        self.speed = speed
        self.cmd = cmd
        
        print "New serial action: %s -> %s" %(name,cmd)
        
    def __repr__(self):
        return "SerialAction %s -> %s %s %s" %(self.name, self.port, self.speed, self.cmd)

    def perform(self):

        print "SerialAction: performing -> %s" %self.cmd

        s = Serial(self.port, self.speed)
        print s
        s.write(self.cmd + "\r")
        s.flush()
        sleep(0.2)
        s.close()
