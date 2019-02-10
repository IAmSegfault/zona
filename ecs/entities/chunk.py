from ecs.entities.entity import Entity
from ecs.components.dimension import Area2D, Volume3D
from ecs.components.position import LoadedMap2D, SuperChunkPosition2D
from ecs.entities.map import Map3D
import numpy as np

class Chunk2D(Entity):
    def __init__(self, world, x, y, w, h, loaded_posX, loaded_posY):
        super().__init__(world, "chunk", ["chunk"])
        world.add_component(self.metadata.entity_id, Area2D(w, h))

        world.add_component(self.metadata.entity_id, LoadedMap2D(loaded_posX, loaded_posY))
        world.add_component(self.metadata.entity_id, SuperChunkPosition2D(x, y))
        area = world.component_for_entity(self.metadata.entity_id, Area2D)
        self.metadata.containers["loaded_maps"] = np.zeros(shape=(area.width, area.height), dtype=np.dtype(object))
