import csv
import numpy as np
import tcod
from os.path import isfile
from game.util.conversion import htmltorgb
from ecs.entities.entity import Entity
from ecs.entities.superchunk import SuperChunk2D
from ecs.components.dimension import Area2D
from ecs.components.init import IsInit
from ecs.components.rng import Rng
class WorldMap(Entity):

    def __init__(self, world, width, height, map_csv, sc_width, sc_height, c_width, c_height, seeds, seed_offsets=None):
        super().__init__(world, "worldmap", ["worldmap"])
        world.add_component(self.metadata.entity_id, Area2D(width, height))
        world.add_component(self.metadata.entity_id, IsInit())
        world.add_component(self.metadata.entity_id, Rng(seeds, seed_offsets))

        self.metadata.containers["superchunks"] = np.zeros((width, height), dtype=np.dtype(object))

        seed_container = world.component_for_entity(self.metadata.entity_id, Rng)


        if isfile(map_csv):
            with open(map_csv) as f:
                reader = csv.reader(f, delimiter=',')
                line_count = 0
                for row in reader:
                    if line_count != 0:
                        x = int(row[0])
                        y = int(row[1])

                        char = chr(int(row[2]))
                        color_fg = htmltorgb(row[3])
                        color_bg = htmltorgb(row[4])
                        sc_seed = tcod.random_get_int(seed_container.generator[0], -2147483647, 2147483647)

                        superchunk = SuperChunk2D(world, sc_width, sc_height, c_width, c_height, x, y, sc_seed,
                                                  char, color_fg, color_bg)
                        self.metadata.containers["superchunks"][x][y] = superchunk.metadata

                    line_count += 1
            isinit = world.component_for_entity(self.metadata.entity_id, IsInit)

            isinit.init = True
        else:
            isinit = world.component_for_entity(self.metadata.entity_id, IsInit)
            isinit.failure = True