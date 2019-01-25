import esper
import logging
import settings
import tcod
import numpy as np
from game.util.constants import Palette
import game.util.constants as constants
from ecs.components.dimension import Area2D
from ecs.components.init import IsInit
from ecs.components.metadata import MetaData
from ecs.components.glyph import Glyph, FOWGlyph
from ecs.components.dimension import WorldFOWCircle
from ecs.components.console import ConsoleHandler
from ecs.components.dimension import Rectangle
from ecs.components.position import WorldMapPosition2D
from ecs.entities.camera import world_to_camera_pos

class WorldMapCameraProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self, render, dirty):
        if render and dirty:
            for camera, (camera_metadata, console_handler, viewport) in self.world.get_components(MetaData, ConsoleHandler, Rectangle):
                if "camera" in camera_metadata.tags and "ascii" in camera_metadata.tags:

                    for world_map, (worldmap_metadata, isinit, area2d) in self.world.get_components(MetaData, IsInit, Area2D):
                        if "worldmap" in worldmap_metadata.tags:

                            if worldmap_metadata.is_hot:
                                x = 0
                                y = 0
                                world_pos = None
                                fov_circle = None
                                for player, (player_metadata, world_map_position, world_fov_circle) in  self.world.get_components(MetaData, WorldMapPosition2D, WorldFOWCircle):
                                    if "player" in player_metadata.tags:
                                        world_pos = world_map_position
                                        fov_circle = world_fov_circle
                                        break

                                radius = fov_circle.radius
                                fov_map = tcod.map_new(area2d.width, area2d.height)
                                for i in range(area2d.width):
                                    for j in range(area2d.height):
                                        superchunk = worldmap_metadata.containers["superchunks"][i][j].entity_id
                                        fow_glyph = self.world.component_for_entity(superchunk, FOWGlyph)
                                        if fow_glyph.character == "^":
                                            tcod.map_set_properties(fov_map, i, j, False, False)
                                        else:
                                            tcod.map_set_properties(fov_map, i, j, True, True)

                                tcod.map_compute_fov(fov_map, world_pos.x, world_pos.y, radius, True, tcod.FOV_SHADOW)

                                shape = worldmap_metadata.containers["superchunks"].shape
                                for i in range(viewport.x1, viewport.x2):
                                    for j in range(viewport.y1, viewport.y2):

                                        if i < 0 or j < 0 or i > shape[0] - 1 or j > shape[1] - 1:
                                            tcod.console_set_default_foreground(console_handler.src_console,
                                                                                Palette.DARKSLATEGRAY.value)
                                            tcod.console_set_char_background(console_handler.src_console, x, y, Palette.DIMGRAY.value)
                                            tcod.console_put_char(console_handler.src_console, x, y, constants.CP437_CHAR_BLOCK2)
                                        else:
                                            superchunk = worldmap_metadata.containers["superchunks"][i][j].entity_id
                                            fow_glyph = self.world.component_for_entity(superchunk, FOWGlyph)
                                            visible = tcod.map_is_in_fov(fov_map, i, j)
                                            if visible:
                                                fow_glyph.visited = True
                                                fow_glyph.in_view = True
                                            else:
                                                fow_glyph.in_view = False

                                            if fow_glyph.visited and fow_glyph.in_view:
                                                tcod.console_set_default_foreground(console_handler.src_console, fow_glyph.color_fg)
                                                tcod.console_set_char_background(console_handler.src_console, x, y,
                                                                                 fow_glyph.color_bg)
                                                tcod.console_put_char(console_handler.src_console, x, y, fow_glyph.character)

                                            elif fow_glyph.visited:
                                                tcod.console_set_default_foreground(console_handler.src_console,
                                                                                    fow_glyph.color_fg_oov)

                                                tcod.console_set_char_background(console_handler.src_console, x, y,
                                                                                 fow_glyph.color_bg_oov)

                                                tcod.console_put_char(console_handler.src_console, x, y,
                                                                      fow_glyph.character)

                                            else:
                                                tcod.console_set_default_foreground(console_handler.src_console,
                                                                                    Palette.DIMGRAY.value)

                                                tcod.console_set_char_background(console_handler.src_console, x, y,
                                                                                 Palette.BLACK.value)

                                                tcod.console_put_char(console_handler.src_console, x, y,
                                                                      constants.CP437_CHAR_BLOCK1)
                                        y += 1
                                    x += 1
                                    y = 0

                                for player, (player_metadata, world_map_position, player_glyph) in self.world.get_components(MetaData, WorldMapPosition2D, Glyph):

                                    if "player" in player_metadata.tags:
                                        tcod.console_set_default_foreground(console_handler.src_console, player_glyph.color_fg)
                                        tcod.console_set_default_background(console_handler.src_console, player_glyph.color_bg)
                                        x, y = world_to_camera_pos(viewport, world_map_position.x, world_map_position.y)
                                        if x is not None and y is not None:
                                            tcod.console_put_char(console_handler.src_console, x, y, player_glyph.character)

                                tcod.console_blit(console_handler.src_console, console_handler.xsrc,
                                                  console_handler.ysrc,
                                                  console_handler.wsrc, console_handler.hsrc,
                                                  console_handler.dst_console,
                                                  console_handler.xdst, console_handler.ydst,
                                                  console_handler.fg_alpha,
                                                  console_handler.bg_alpha)
                                break


