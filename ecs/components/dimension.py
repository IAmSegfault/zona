class Volume3D(object):
    def __init__(self, width, height, length):
        self.width = width
        self.height = height
        self.length = length


class Area2D(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height


class Circle(object):
    def __init__(self, radius):
        self.radius = radius


class WorldFOWCircle(Circle):
    def __init__(self, radius):
        super().__init__(radius)

class MapFOWCircle(Circle):
    def __init__(self, radius):
        super().__init__(radius)

class Rectangle(object):
    def __init__(self,x1, y1, x2, y2):
        # Upper left hand corner
        self.x1 = x1
        self.y1 = y1
        # Lower right hand corner
        self.x2 = x2
        self.y2 = y2