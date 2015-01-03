#!/usr/bin/python

import sys
import os
import StringIO
from string import maketrans

import xml.etree.cElementTree as ET

from EIBConnection import EIBBuffer
from EIBConnection import EIBConnection

from event import Event
from serialaction import SerialAction
from knxmonitor_pdu import KnxPdu

eventlist = {}
actionlist = {}

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print "usage: %s url" % sys.argv[0];
        sys.exit(1);

    dom = ET.parse("knxcontrol.xml")
    config = dom.getroot()

    events = config.find("events").findall("event")
    for e in events:

        E = Event(e.attrib["name"],
                  e.attrib["groupaddr"],
                  e.attrib["value"])

        eventlist[E.name] = E

    actions = config.find("actions").findall("action")
    for a in actions:
        
        name = a.attrib["name"]
        aa = a.find("serialAction")
        if aa != None:

            A = SerialAction(name,
                             aa.attrib["port"],
                             aa.attrib["speed"],
                             aa.attrib["cmdString"])

        else:
            ab = a.find("knxAction")
            if ab != None:
                # Ignore for now, TBC...
                continue
            else:
                print "Unknown action type..."
                sys.exit(1)

        actionlist[A.name] = A

    logic = config.find("logic").findall("onEvent")
    for oe in logic:

        eventlist[oe.attrib["eventName"]].addAction(oe.attrib["actionName"])

    try:
        con = EIBConnection()
    except:
        print "Could not instantiate EIBConnection";
        sys.exit(1);
        
    if con.EIBSocketURL(sys.argv[1]) != 0:
        print "Could not connect to: %s" %sys.argv[1]
        sys.exit(1)
        
        
    if con.EIBOpenVBusmonitorText() != 0:
        print "Could not open bus monitor";
        # sys.exit(1)

    buf = EIBBuffer()
    while 1:
        length = con.EIBGetBusmonitorPacket (buf)
        if length == 0:
            print "Read failed"
            sys.exit(1)

        # Map buffer to string...
        b = ""
        for x in buf.buffer:
            b += chr(x)
        #print b
        
        pdu = KnxPdu({}, {}, b)

        for k,e in eventlist.items():
            actions = e.match(pdu.getTo(), pdu.getValue(None))
            for a in actions:
                actionlist[a].perform()

    con.EIBClose()

