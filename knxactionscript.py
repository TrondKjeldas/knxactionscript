#!/usr/bin/python

import sys

from knxactionscript.knxactionscript import KnxActionScript
from knxactionscript.knxmonitor_pdu import KnxPdu
from knxactionscript.EIBConnection import EIBBuffer
from knxactionscript.EIBConnection import EIBConnection


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("usage: %s cfg url" % sys.argv[0])
        sys.exit(1)

    KAS = KnxActionScript(sys.argv[1])

    sys.exit(0)

    con = EIBConnection()

    if con.EIBSocketURL(sys.argv[1]) != 0:
        print("Could not connect to: %s" % sys.argv[1])
        sys.exit(1)

    if con.EIBOpenVBusmonitorText() != 0:
        print("Could not open bus monitor")
        # sys.exit(1)

    buf = EIBBuffer()
    while 1:
        length = con.EIBGetBusmonitorPacket(buf)
        if length == 0:
            print("Read failed")
            sys.exit(1)

        # Map buffer to string...
        b = ""
        for x in buf.buffer:
            b += chr(x)
        # print b

        pdu = KnxPdu({}, {}, b)

        KAS.handle(pdu)

    con.EIBClose()
