class Position3D(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class Position2D(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class MapPosition3D(Position3D):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)


class ChunkPosition2D(Position2D):
    def __init__(self, x, y):
        super().__init__(x, y)


class SuperChunkPosition2D(Position2D):
    def __init__(self, x, y):
        super().__init__(x, y)


class WorldMapPosition2D(Position2D):
    def __init__(self, x, y):
        super().__init__(x, y)

class LoadedChunk2D(Position2D):
    def __init__(self, x, y):
        super().__init__(x, y)

class LoadedMap2D(Position2D):
    def __init__(self, x, y):
        super().__init__(x, y)