from time import sleep

from serialports import SerialPort


class SerialAction:

    def __init__(self, name, port, speed, cmd):
        self.name = name
        self.port = port
        self.speed = speed
        self.cmd = cmd

        print("New serial action: %s -> %s" % (name, cmd))

        # self.portObj = SerialPort(port, speed)

    def __repr__(self):
        return "SerialAction %s -> %s %s %s" % (self.name, self.port,
                                                self.speed, self.cmd)

    def perform(self):

        print("SerialAction: performing -> %s" % self.cmd)

        self.portObj.write(self.cmd + "\r")

    def quit(self):
        self.portObj.quit()


if __name__ == "__main__":

    a = SerialAction("A", "/dev/ttyACM1", 9600, "SET RO 9 1")
    b = SerialAction("B", "/dev/ttyACM1", 9600, "SET RO 9 0")

    print(a)
    print(b)

    sleep(1)
    a.perform()
    sleep(1)
    b.perform()
    sleep(1)
    a.perform()
    sleep(1)
    b.perform()

    a.quit()
    b.quit()
