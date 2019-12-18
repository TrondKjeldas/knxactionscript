

class Event(object):

    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.actions = []
        print("New event: %s -> %s" % (name, value))

    def __repr__(self):
        return "KNX Event %s %s -> %s" % (self.name, self.value, self.actions)

    def addAction(self, actionname):
        self.actions.append(actionname)

    def match(self, value):
        if value == self.value or self.value == "*":
            return self.actions

        # print "%s did not match %s %s" %(self, groupaddr, value)
        return []
