#!/usr/bin/python

import sys
import os
import StringIO
from string import maketrans

import xml.etree.cElementTree as ET

from EIBConnection import EIBBuffer
from EIBConnection import EIBConnection

eventlist = []
cache = {}


class Event():

    def __init__(self, gaddr, value):

        self.gaddr = gaddr
        self.value = value

        self.actions = []

    def __repr__(self):
        return "xxx"

    def addAction(self, action):

        self.actions.append(action)

    def received(self, gaddr, value):

        if gaddr == self.gaddr and value == self.value:
            for a in self.actions:
                a.run()

class Condition():

    def __init__(self, gaddr=None, value=None, oper=None, name=None):

        self.subconditions = None

        self.name = name if name != None else ""
        
        if oper != None:
            if gaddr != None or value != None:
                print ("can not have groupaddress or value "
                       "on operator condition")
                sys.exit(1)
            else:
                self.oper = oper
                self.gaddr = None
                self.value = None
                return

        if gaddr == None or value == None:
            print ("must provide both groupaddress and "
                   "value for non-operator conditions")
            sys.exit(1)

        self.gaddr = gaddr
        self.value = value
        self.oper  = None

    def __repr__(self):
        if self.oper != None:
            s =  "condition %s: operator '%s' - " %(self.name, self.oper)
            s += "with subconditions '%s'" %self.subconditions
            return s
        else:
            return "condition %s: %s - %s" %(self.name, self.gaddr, self.value)

    def isMet(self):
        print "checking %s" %self.name
        
        if self.oper == "and":
            for c in self.subconditions:
                if not c.isMet():
                    print "condition '%s' is not met!" %c.name
                    return False
            return True
        
        elif self.oper == "or":
            names = ""
            for c in self.subconditions:
                if c.isMet():
                    return True
                names += "/%s" %c.name
            print "neither of conditions '%s' is met!"%names[1:] 
            return False

        else:
            if self.gaddr in cache.keys():
                if cache[self.gaddr] == self.value:
                    return True
            print "condition '%s' is not met!" %self.name
            return False

        print "ERROR! should never get here!"
        return False
        
    def addSubConditions(self, conditions):
        #print "  adding subcondition: %s" %conditions
        self.subconditions = conditions

    
class Action():

    def __init__(self, gaddr, value):

        self.gaddr = gaddr
        self.value = value

        self.condition = None

    def __repr__(self):
        return "xxx"
    
    def addCondition(self, condition):

        print "adding: %s" %condition
        self.condition = condition

    def run(self):
        
        #print "%s-%s: %s" %(self.gaddr, self.value, self.condition)
        if self.condition and not self.condition.isMet():
            return
            
        print "running action: %s %s" %(self.gaddr, self.value)


def parseConditions(conditions, operator):

    conds = []
    for c in conditions:
        #print c
        name = c.attrib["name"] if "name" in c.attrib.keys() else ""
            
        if "groupaddr" in c.attrib.keys():
            C = Condition(c.attrib["groupaddr"],
                          c.attrib["value"], name=name)
        else:
            C = Condition(oper = c.attrib["operator"], name=name)
        sub = c.findall("condition")
        #print sub
        if len(sub) > 0:
            C.addSubConditions(parseConditions(sub, operator))
        conds.append(C)

    if len(conds) > 0:
        #print "returning: %s" % conds
        return conds
    else:
        #print "returning: None"
        return None

def receiver(g, v):

    cache[g] = v
    for e in eventlist:
        e.received(g, v)

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print "usage: %s url" % sys.argv[0];
        sys.exit(1);

    dom = ET.parse("knxcontrol.xml")
    root = dom.getroot()

    events = root.findall("event")
    for e in events:

        E = Event(e.attrib["groupaddr"],
                  e.attrib["value"])

        actions = e.findall("action")
        for a in actions:

            A = Action(a.attrib["groupaddr"],
                       a.attrib["value"])

             # Only one condition allower on outer level
            condition = a.find("condition")
            if condition != None:
                C = parseConditions([condition], None)
                # The parseConditions function should always return
                # a list with 1 element in this situation, in which
                # we want to remove the list...
                A.addCondition(C[0])

            E.addAction(A)

        eventlist.append(E)

        
    
    try:
        con = EIBConnection()
    except:
        print "Could not instanciate EIBConnection";
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

        print b

    con.EIBClose()

    # Simulate reception of telegrams...
    receiver("1/1/0", "5")
    receiver("2/6/0", "5")
    receiver("2/6/1", "4")
    receiver("9/6/0", "3")
    receiver("1/1/0", "5")
    receiver("2/6/0", "0")
    receiver("5/1/0", "15")
