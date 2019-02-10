from ecs.entities.entity import Entity
from ecs.entities.maptile import MapTile
from ecs.components.position import Position2D
from ecs.components.dimension import Volume3D, Height
from ecs.components.init import IsInit
from ecs.components.glyph import FOWGlyph
from ecs.components.vicinity import Vicinity
from game.util.conversion import htmltorgb
from ecs.enum.vicinity import *
from os.path import isfile
import csv
import numpy as np

class Map3D(Entity):
    def __init__(self, world, width, height, length, x, y, curr_height, load_static=False):
        tags = ["Map3D"]
        templates = None
        super().__init__(world, "Map3D", tags, templates)

        #dimensions of the contained map
        world.add_component(self.metadata.entity_id, Volume3D(width, height, length))

        #position in the containing chunk
        world.add_component(self.metadata.entity_id, Position2D(x, y))

        world.add_component(self.metadata.entity_id, Height(curr_height))

        world.add_component(self.metadata.entity_id, IsInit())

        self.metadata.containers["map_tiles"] = np.empty(shape=(width, height, length), dtype=np.dtype(object))
        for i in range(0, width):
            for j in range(0, length):
                    map_tile = MapTile(world, i, curr_height, j)
                    self.metadata.containers["map_tiles"][i][curr_height][j] = map_tile.metadata

        if not load_static:
            pass
        else:
            if isfile(load_static):
                with open(load_static) as f:
                    reader = csv.reader(f, delimiter=',')
                    line_count = 0
                    for row in reader:
                        if line_count != 0:
                            x = int(row[0])
                            z = int(row[1])
                            char = int(row[2])
                            fg_hex = row[3]
                            bg_hex = row[4]
                            color_fg = htmltorgb(row[3])
                            color_bg = htmltorgb(row[4])
                            mt_metadata = self.metadata.containers["map_tiles"][x][curr_height][z]
                            fow_glyph = world.component_for_entity(mt_metadata.entity_id, FOWGlyph)
                            fow_glyph.character = char
                            vtype = None
                            for vt in VicinityType:
                                if char == vt.value.character and bg_hex == vt.value.id:
                                    vicinity = world.component_for_entity(mt_metadata.entity_id, Vicinity)
                                    vicinity.vtype = vt.value
                                    vicinity.supertype = vt.value.supertype
                                    vicinity.transparent = vt.value.transparent
                                    vicinity.walkable = vt.value.walkable
                                    vtype = str(vt.name)
                                    break

                            fow_glyph.color_fg = color_fg
                            fow_glyph.color_bg = color_bg

                            for vcol in VicinityColor:
                                if vcol.name == vtype:
                                    fow_glyph.color_fg = vcol.value[0].value
                                    fow_glyph.color_bg = vcol.value[1].value
                                    break

                        line_count += 1