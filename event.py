
class Event:
    
    def __init__(self, name, groupaddr, value):
        self.name = name
        self.groupaddr = groupaddr
        self.value = value
        self.actions = []

        print "New event: %s -> %s %s" %(name, groupaddr, value)

    def __repr__(self):
        return "Event %s %s %s -> %s" %(self.name, self.groupaddr, self.value, self.actions)

    def addAction(self, actionname):
        self.actions.append(actionname)

    def match(self, groupaddr, value):
        if groupaddr == self.groupaddr:
            if value == self.value or value == "*":
                return self.actions
                
        #print "%s did not match %s %s" %(self, groupaddr, value)
        return []

                
