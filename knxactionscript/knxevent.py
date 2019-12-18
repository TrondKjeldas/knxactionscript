
from event import Event


class KnxEvent(Event):

    def __init__(self, name, groupaddr, value):
        Event.__init__(self, name, value)
        self.groupaddr = groupaddr

        print("New KNX event: %s -> %s %s" % (name, groupaddr, value))

    def __repr__(self):
        return "KNX Event %s %s %s -> %s" % (self.name, self.groupaddr,
                                             self.value, self.actions)

    def match(self, groupaddr, value):
        if groupaddr == self.groupaddr:
            return Event.match(self, value)

        # print "%s did not match %s %s" %(self, groupaddr, value)
        return []
