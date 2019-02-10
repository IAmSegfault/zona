class Actor(object):
    def __init__(self, speed, is_playercharacter=False):
        self.speed = speed
        self.scenestate = "init"
        self.is_playercharacter = is_playercharacter
        self.ct = 60