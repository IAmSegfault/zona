class IsInit(object):
    def __init__(self, event=None, args=None):
        self.init = False
        self.trigger = False
        self.failure = False
        self.event = event
        self.args = args