class Player(object):
    def __init__(self, player_class):
        self.player_class = player_class
        self.level = 1
        self.xp = 0
        self.slots = []
        self.groups = []