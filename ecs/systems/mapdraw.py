import esper
import tcod
from game.util.constants import Palette
import game.util.constants as constants
from ecs.components.dimension import Area2D
from ecs.components.init import IsInit
from ecs.components.metadata import MetaData
from ecs.components.glyph import Glyph, FOWGlyph
from ecs.components.dimension import WorldFOWCircle
from ecs.components.console import ConsoleHandler
from ecs.components.dimension import Rectangle, Volume3D
from ecs.components.position import WorldMapPosition2D, SuperChunkPosition2D, ChunkPosition2D, MapPosition3D
from ecs.components.vicinity import Vicinity
from ecs.components.light import LightRadius
from ecs.entities.camera import world_to_camera_pos


class WorldMapCameraProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def _get_player_components(self, ):
        for player, (player_metadata, world_map_position, world_fov_circle) in self.world.get_components(MetaData,
                                                                                                         WorldMapPosition2D,
                                                                                                         WorldFOWCircle):
            if "player" in player_metadata.tags:
                return world_map_position, world_fov_circle

    def _compute_fov(self, fov_map, area2d, worldmap_metadata, world_pos, radius):
        for i in range(area2d.width):
            for j in range(area2d.height):
                superchunk = worldmap_metadata.containers["superchunks"][i][j].entity_id
                fow_glyph = self.world.component_for_entity(superchunk, FOWGlyph)
                if fow_glyph.character == "^":
                    tcod.map_set_properties(fov_map, i, j, False, False)
                else:
                    tcod.map_set_properties(fov_map, i, j, True, True)

        tcod.map_compute_fov(fov_map, world_pos.x, world_pos.y, radius, True, tcod.FOV_SHADOW)

    def _draw_oob(self, console_handler, x, y):
        tcod.console_set_default_foreground(console_handler.src_console,
                                            Palette.DARKSLATEGRAY.value)
        tcod.console_set_char_background(console_handler.src_console, x, y, Palette.DIMGRAY.value)
        tcod.console_put_char(console_handler.src_console, x, y, constants.CP437_CHAR_BLOCK2)

    def _draw_in_view(self, console_handler, x, y, fow_glyph):
        tcod.console_set_default_foreground(console_handler.src_console, fow_glyph.color_fg)
        tcod.console_set_char_background(console_handler.src_console, x, y,
                                         fow_glyph.color_bg)
        tcod.console_put_char(console_handler.src_console, x, y, fow_glyph.character)

    def _draw_visited_fow(self, console_handler, x, y, fow_glyph):
        tcod.console_set_default_foreground(console_handler.src_console,
                                            Palette.DARKSLATEGRAY.value)

        tcod.console_set_char_background(console_handler.src_console, x, y,
                                         Palette.BLACK.value)

        tcod.console_put_char(console_handler.src_console, x, y,
                              fow_glyph.character)

    def _draw_fow(self, console_handler, x, y):
        tcod.console_set_default_foreground(console_handler.src_console,
                                            Palette.DIMGRAY.value)

        tcod.console_set_char_background(console_handler.src_console, x, y,
                                         Palette.BLACK.value)

        tcod.console_put_char(console_handler.src_console, x, y,
                              constants.CP437_CHAR_BLOCK1)

    def _draw_world(self, worldmap_metadata, viewport, fov_map, console_handler):
        x = 0
        y = 0
        shape = worldmap_metadata.containers["superchunks"].shape
        for i in range(viewport.x1, viewport.x2):
            for j in range(viewport.y1, viewport.y2):

                if i < 0 or j < 0 or i > shape[0] - 1 or j > shape[1] - 1:
                    self._draw_oob(console_handler, x, y)
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
                        self._draw_in_view(console_handler, x, y, fow_glyph)
                    elif fow_glyph.visited:
                        self._draw_visited_fow(console_handler, x, y, fow_glyph)
                    else:
                        self._draw_fow(console_handler, x, y)
                y += 1
            x += 1
            y = 0

    def _draw_player(self, console_handler, viewport):
        for player, (player_metadata, world_map_position, player_glyph) in self.world.get_components(MetaData,
                                                                                                     WorldMapPosition2D,
                                                                                                     Glyph):
            if "player" in player_metadata.tags:
                tcod.console_set_default_foreground(console_handler.src_console, player_glyph.color_fg)
                tcod.console_set_default_background(console_handler.src_console, player_glyph.color_bg)
                x, y = world_to_camera_pos(viewport, world_map_position.x, world_map_position.y)
                if x is not None and y is not None:
                    tcod.console_put_char(console_handler.src_console, x, y, player_glyph.character)

    def _blit(self, console_handler):
        tcod.console_blit(console_handler.src_console, console_handler.xsrc, console_handler.ysrc,
                          console_handler.wsrc, console_handler.hsrc, console_handler.dst_console,
                          console_handler.xdst, console_handler.ydst, console_handler.fg_alpha,
                          console_handler.bg_alpha)

    def process(self, *args, **kwargs):
        if kwargs["render"] and kwargs["dirty"] and not kwargs["local_render"]:
            for camera, (camera_metadata, console_handler, viewport) in self.world.get_components(MetaData, ConsoleHandler, Rectangle):
                if "camera" in camera_metadata.tags and "ascii" in camera_metadata.tags and "worldmap" in camera_metadata.tags:

                    for world_map, (worldmap_metadata, isinit, area2d) in self.world.get_components(MetaData, IsInit, Area2D):
                        if "worldmap" in worldmap_metadata.tags:

                            if worldmap_metadata.is_hot:
                                world_pos = None
                                fov_circle = None
                                world_pos, fov_circle = self._get_player_components()
                                radius = fov_circle.radius
                                fov_map = tcod.map_new(area2d.width, area2d.height)
                                self._compute_fov(fov_map, area2d, worldmap_metadata, world_pos, radius)
                                self._draw_world(worldmap_metadata, viewport, fov_map, console_handler)
                                self._draw_player(console_handler, viewport)
                                self._blit(console_handler)
                                break


class LocalMapCameraProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def _get_player_components(self):
        for player, (player_metadata, wm_pos, sc_pos, c_pos, m_pos, l_radius) in \
                self.world.get_components(MetaData, WorldMapPosition2D, SuperChunkPosition2D, ChunkPosition2D,
                                          MapPosition3D, LightRadius):
            if "player" in player_metadata.tags:
                return wm_pos, sc_pos, c_pos, m_pos, l_radius

    def _get_local_map(self, world_map_pos, superchunk_pos, chunk_pos):
        for world_map, worldmap_metadata in self.world.get_components(MetaData):
            worldmap_metadata = worldmap_metadata[0]
            if "worldmap" in worldmap_metadata.tags:
                superchunk = worldmap_metadata.containers["superchunks"][world_map_pos.x][world_map_pos.y]
                chunk = superchunk.containers["loaded_chunks"][superchunk_pos.x][superchunk_pos.y]
                map3d = chunk.containers["loaded_maps"][chunk_pos.x][chunk_pos.y]

                return superchunk, chunk, map3d

    def _draw_oob(self, console_handler, x, y):
        tcod.console_set_default_foreground(console_handler.src_console,
                                            Palette.DARKSLATEGRAY.value)
        tcod.console_set_char_background(console_handler.src_console, x, y, Palette.DIMGRAY.value)
        tcod.console_put_char(console_handler.src_console, x, y, constants.CP437_CHAR_BLOCK2)

    def _draw_actor(self, console_handler, maptile_metadata, x, z):
        actor_metadata = maptile_metadata.containers["actors"][-1]
        actor_glyph = self.world.component_for_entity(actor_metadata.entity_id, Glyph)
        tcod.console_set_default_foreground(console_handler.src_console,
                                            actor_glyph.color_fg)
        tcod.console_set_default_background(console_handler.src_console,
                                            actor_glyph.color_bg)
        tcod.console_put_char(console_handler.src_console, x, z, actor_glyph.character)

    def _draw_static_actor(self, console_handler, maptile_metadata, x, z):
        static_actor_metadata = maptile_metadata.containers["static_actors"][-1]
        static_actor_glyph = self.world.component_for_entity(static_actor_metadata.entity_id, Glyph)
        tcod.console_set_default_foreground(console_handler.src_console,
                                            static_actor_glyph.color_fg)
        tcod.console_set_default_background(console_handler.src_console,
                                            static_actor_glyph.color_bg)
        tcod.console_put_char(console_handler.src_console, x, z, static_actor_glyph.character)

    def _draw_vicinity(self, console_handler, fow_glyph_vicinity, x, z):
        tcod.console_set_default_foreground(console_handler.src_console,
                                            fow_glyph_vicinity.color_fg)

        tcod.console_set_char_background(console_handler.src_console, x, z,
                                         fow_glyph_vicinity.color_bg)

        tcod.console_put_char(console_handler.src_console, x, z,
                              fow_glyph_vicinity.character)

    def _draw_visited_fow(self, console_handler, fow_glyph_vicinity, x, z):
        tcod.console_set_default_foreground(console_handler.src_console,
                                            Palette.DARKSLATEGRAY.value)

        tcod.console_set_char_background(console_handler.src_console, x, z,
                                         Palette.BLACK.value)

        tcod.console_put_char(console_handler.src_console, x, z,
                              fow_glyph_vicinity.character)

    def _draw_fow(self, console_handler, x, z):
        tcod.console_set_default_foreground(console_handler.src_console,
                                            Palette.DIMGRAY.value)

        tcod.console_set_char_background(console_handler.src_console, x, z,
                                         Palette.BLACK.value)

        tcod.console_put_char(console_handler.src_console, x, z,
                              constants.CP437_CHAR_BLOCK1)

    def _draw_player(self, console_handler, viewport):
        for player, (player_metadata, local_map_position, player_glyph) in self.world.get_components(MetaData,
                                                                                                     MapPosition3D,
                                                                                                     Glyph):
            if "player" in player_metadata.tags:
                tcod.console_set_default_foreground(console_handler.src_console, player_glyph.color_fg)
                tcod.console_set_default_background(console_handler.src_console, player_glyph.color_bg)
                x, y = world_to_camera_pos(viewport, local_map_position.x, local_map_position.z)
                if x is not None and y is not None:
                    tcod.console_put_char(console_handler.src_console, x, y, player_glyph.character)

    def _blit(self, console_handler):
        tcod.console_blit(console_handler.src_console, console_handler.xsrc, console_handler.ysrc,
                          console_handler.wsrc, console_handler.hsrc, console_handler.dst_console,
                          console_handler.xdst, console_handler.ydst, console_handler.fg_alpha,
                          console_handler.bg_alpha)

    def process(self, *args, **kwargs):
        if kwargs["render"] and kwargs["dirty"] and kwargs["local_render"]:
            for camera, (camera_metadata, console_handler, viewport) in self.world.get_components(MetaData, ConsoleHandler, Rectangle):
                if "camera" in camera_metadata.tags and "ascii" in camera_metadata.tags and "localmap" in camera_metadata.tags:
                    world_map_pos = None
                    superchunk_pos = None
                    chunk_pos = None
                    map_pos = None
                    superchunk = None
                    chunk = None
                    map3d = None
                    light_radius = None
                    world_map_pos, superchunk_pos, chunk_pos, map_pos, light_radius = self._get_player_components()
                    superchunk, chunk, map3d = self._get_local_map(world_map_pos, superchunk_pos, chunk_pos)

                    if map3d is not None and map3d.is_hot:
                        vol = self.world.component_for_entity(map3d.entity_id, Volume3D)
                        fov_map = tcod.map_new(vol.width, vol.length)
                        for i in range(vol.width):
                            for j in range(vol.length):
                                maptile_metadata = map3d.containers["map_tiles"][i][map_pos.y][j]
                                vicinity = self.world.component_for_entity(maptile_metadata.entity_id, Vicinity)
                                tcod.map_set_properties(fov_map, i, j, vicinity.transparent, vicinity.walkable)

                        tcod.map_compute_fov(fov_map, map_pos.x, map_pos.z, light_radius.radius, True, tcod.FOV_SHADOW)
                        x = 0
                        z = 0
                        shape = map3d.containers["map_tiles"].shape
                        for i in range(viewport.x1, viewport.x2):
                            for j in range(viewport.y1, viewport.y2):
                                if i < 0 or j < 0 or i > shape[0] - 1 or j > shape[2] - 1:

                                    self._draw_oob(console_handler, x, z)
                                else:
                                    maptile_metadata = map3d.containers["map_tiles"][i][map_pos.y][j]
                                    use_actor = False
                                    use_static_actor = False
                                    fow_glyph_vicinity = self.world.component_for_entity(maptile_metadata.entity_id, FOWGlyph)
                                    visible = tcod.map_is_in_fov(fov_map, i, j)
                                    if visible:
                                        fow_glyph_vicinity.visited = True
                                        fow_glyph_vicinity.in_view = True
                                    else:
                                        fow_glyph_vicinity.in_view = False

                                    if fow_glyph_vicinity.visited and fow_glyph_vicinity.in_view:
                                        if len(maptile_metadata.containers["actors"]) > 0:
                                            use_actor = True
                                        elif len(maptile_metadata.containers["static_actors"]) > 0:
                                            use_static_actor = True

                                        if use_actor:
                                            self._draw_actor(console_handler, maptile_metadata, x, z)
                                        elif use_static_actor:
                                            self._draw_static_actor(console_handler, maptile_metadata, x, z)
                                        else:
                                            self._draw_vicinity(console_handler, fow_glyph_vicinity, x, z)

                                    elif fow_glyph_vicinity.visited:
                                        self._draw_visited_fow(console_handler, fow_glyph_vicinity, x, z)
                                    else:
                                        self._draw_fow(console_handler, x, z)
                                z += 1
                            x += 1
                            z = 0
                        self._draw_player(console_handler, viewport)
                        self._blit(console_handler)
                    break
