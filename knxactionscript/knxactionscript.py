#!/usr/bin/python

import sys
import xml.etree.cElementTree as ET

from knxevent import KnxEvent
from serialaction import SerialAction


class KnxActionScript(object):

    def __init__(self, configfile):

        self.eventlist = {}
        self.actionlist = {}

        dom = ET.parse(configfile)
        config = dom.getroot()

        events = config.find("events").findall("event")
        for e in events:

            E = KnxEvent(e.attrib["name"],
                         e.attrib["groupaddr"],
                         e.attrib["value"])

            self.eventlist[E.name] = E

        actions = config.find("actions").findall("action")
        for a in actions:
            name = a.attrib["name"]
            aa = a.find("serialAction")
            if aa is not None:
                A = SerialAction(name,
                                 aa.attrib["port"],
                                 aa.attrib["speed"],
                                 aa.attrib["cmdString"])
            else:
                ab = a.find("knxAction")
                if ab is not None:
                    # Ignore for now, TBC...
                    continue
                else:
                    print("Unknown action type...")
                    sys.exit(1)

            self.actionlist[A.name] = A

        logic = config.find("logic").findall("onEvent")
        for oe in logic:
            self.eventlist[oe.attrib["eventName"]].addAction(
                                                oe.attrib["actionName"])

        sys.exit(0)

    def handle(self, pdu):

            for k, e in self.eventlist.items():
                actions = e.match(pdu.getTo(), pdu.getValue(None))
                for a in actions:
                    self.actionlist[a].perform()
