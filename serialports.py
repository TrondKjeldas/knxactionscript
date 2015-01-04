from serial import Serial
from time import sleep
from threading import Thread

running_threads = {}
callBacks = {}
open_ports = {}

class SerialPort:

    def __init__(self, port, speed):
        self.port = port
        self.speed = speed
        
        print "New serial port: %s" %(port)

        if self.port not in open_ports.keys():
            print "SerialPort: Opening %s" %self.port
            open_ports[self.port] = Serial(self.port, self.speed)
            sleep(1)
            open_ports[self.port].setTimeout(1)
            open_ports[self.port].write("\r")

        if self.port not in running_threads.keys():
            t = Thread(name="T_%s"%port, target=self.run, args=[self.port])
            running_threads[self.port] = t
            t.start()
        
    def __repr__(self):
        return "SerialPort: %s %s" %(self.port, self.speed)

    def write(self, string):
        open_ports[self.port].write(string)
        open_ports[self.port].flush()

    def run(self, port):

        #print "SerialPort: starting thread..."
        print port
        while port in running_threads.keys():
            string = open_ports[port].readline()
            string = string.strip()
            if len(string)>0:
                if port in callBacks.keys():
                    for cb in callBacks[port]:
                        cb(string)
        print "SerialPort: ending thread..."

    def addCallback(self, callBack):

        if not self.port in callBacks.keys():
            callBacks[self.port] = []

        callBacks[self.port].append(callBack)

    def quit(self):
        if self.port in running_threads.keys():
            t = running_threads[self.port]
            running_threads.pop(self.port, None)
            t.join()
    

if __name__ == "__main__":

    def cb1(string):
        print "cb1: #%s#" %string
    def cb2(string):
        print "cb2: #%s#" %string

    a = SerialPort("/dev/ttyACM1", 9600)
    b = SerialPort("/dev/ttyACM1", 9600)

    print a
    print b

    a.addCallback(cb1)
    b.addCallback(cb2)

    sleep(0.5)
    a.write("SET RO 9 1\r")
    sleep(0.5)
    b.write("SET RO 9 0\r")
    sleep(0.5)
    a.write("SET RO 9 1\r")
    sleep(0.5)
    b.write("SET RO 9 0\r")
    sleep(0.5)
    a.write("GET DI 3\r")
    sleep(0.5)
    b.write("GET AI 15\r")
    sleep(2)
    a.quit()
    b.quit()
