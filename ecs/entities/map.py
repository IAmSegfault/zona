from ecs.entities.entity import Entity
from ecs.entities.maptile import MapTile
from ecs.components.position import Position2D
from ecs.components.dimension import Volume3D
from ecs.components.init import IsInit
import numpy as np


class Map3D(Entity):
    def __init__(self, world, width, height, length, x, y):
        tags = ["Map3D"]
        templates = None
        super().__init__(world, "Map3D", tags, templates)

        #dimensions of the contained map
        world.add_component(self.metadata.entity_id, Volume3D(width, height, length))

        #position in the containing chunk
        world.add_component(self.metadata.entity_id, Position2D(x, y))

        world.add_component(self.metadata.entity_id, IsInit())

        self.metadata.containers["map_tiles"] = np.empty(shape=(width, height, length), dtype=np.dtype(object))
        for i in range(0, width):
            for j in range(0, height):
                for k in range(0, length):
                    map_tile = MapTile(world, i, j, k)
                    self.metadata.containers["map_tiles"][i][j][k] = map_tile.metadata
