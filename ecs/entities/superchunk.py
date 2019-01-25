import numpy as np
import tcod
from ecs.entities.entity import Entity
from ecs.components.chunk import ChunkLoader
from ecs.components.position import WorldMapPosition2D
from ecs.components.dimension import Area2D
from ecs.components.glyph import FOWGlyph
from ecs.components.init import IsInit
from ecs.components.rng import Rng


class SuperChunk2D(Entity):
    def __init__(self, world, width, height, chunk_width, chunk_height, x, y, seed, character, color_fg, color_bg=None):
        super().__init__(world, "SuperChunk2D", ["SuperChunk2D"])
        world.add_component(self.metadata.entity_id, IsInit())

        # The position of the superchunk in the world.
        world.add_component(self.metadata.entity_id, WorldMapPosition2D(x, y))
        # The number of chunks in the superchunk
        world.add_component(self.metadata.entity_id, Area2D(width, height))
        world.add_component(self.metadata.entity_id, FOWGlyph(character, color_fg, color_bg))
        world.add_component(self.metadata.entity_id, Rng([seed]))

        rng = world.component_for_entity(self.metadata.entity_id, Rng)
        self.metadata.containers["loaded_chunks"] = np.zeros(shape=(chunk_width, chunk_height), dtype=np.dtype(object))
        self.metadata.containers["chunk_seeds"] = np.zeros(shape=(chunk_width, chunk_height), dtype=np.int32)

        x = 0
        y = 0
        for i in range(chunk_width):
            for j in range(chunk_height):
                self.metadata.containers["chunk_seeds"][x][y] = tcod.random_get_int(rng.generator[0], -2147483647, 2147483647)
                y += 1
            x += 1
            y = 0

