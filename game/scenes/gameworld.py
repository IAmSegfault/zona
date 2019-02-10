import settings
import tcod
import json
import logging
import os
import game.util.constants as constants
from os.path import isfile
from game.scene import Scene
from ecs.entities.worldmap import WorldMap
from ecs.entities.camera import AsciiCamera
from ecs.entities.player import PlayerCharacter
from ecs.entities.chunk import Chunk2D
from ecs.entities.map import Map3D
from ecs.components.dimension import ChunkArea2D
from ecs.components.position import WorldMapPosition2D, SuperChunkPosition2D, ChunkPosition2D, MapPosition3D
from ecs.systems.mapdraw import WorldMapCameraProcessor, LocalMapCameraProcessor
from ecs.systems.chargetime import CTProcessor
from game.util.input import InputMap
from gui.menu import GameMenu, MessageLog
from game.kernel.gameworldkernel import GameWorldKernel
from game.kernel.uikernel import UIKernel
from ecs.events.mapevent import *


class GameWorldScene(Scene):

    def __init__(self, manager):
        super().__init__(manager)
        self.console["game_world"] = tcod.console_new(settings.CONSOLE_WIDTH, settings.CONSOLE_HEIGHT)
        self.input_action_queue = {}
        self.input_action_queue["init"] = []
        self.input_action_queue["world_map"] = []
        self.input_action_queue["local_map"] = []
        self.input_action_queue["player_at"] = []
        self.state = "init"
        self.static_map = []
        self.world_map = None
        self.world_map_camera = None
        self.world_map_camera_processor = None
        self.local_map_camera_processor = None
        self.ct_processor=None
        self.game_menu = None
        self.message_log = None
        self.player = None
        self.graphics_dirty = True
        self.local_render = True
        self.input_map = None
        self.gwk = None
        self.uik = None
        self.map_events = MapEvents()
        self.map_events.move_local_map_doing += local_map_walk
        self.map_events.move_local_map_end += walk_energy_deplete

        self.map_events.mob_move_local_map_doing += mob_local_map_walk
        self.map_events.mob_move_local_map_end += walk_energy_deplete
    def state_change(self, state):
        prev_state = self.state
        self.state = state


    def init_scene(self):
        directive_path = settings.TEMP_DIR + "/bootloader.json"
        directive = None
        if isfile(directive_path):
            with open(directive_path) as f:
                directive = json.load(f)
        else:
            logging.basicConfig(filename=settings.LOG_FILE,
                                format='%(asctime)s - %(name)s - %(levelname)s: %(message)s')
            logging.critical("Could not read directive at %s" % directive_path)
            exit(1)

        new_character = False
        if directive["init_mode"] == "new_game":
            new_character = True

        self.input_map = InputMap({}, {}, {})
        self.input_map.set_keyset(settings.GAMEWORLD_INPUT)
        if new_character:
            self.player = PlayerCharacter(self.storage, new_character, directive["character"])
            position = directive["position"]

            self.storage.add_component(self.player.metadata.entity_id, WorldMapPosition2D(position["world_map_pos"][0],
                                                                                          position["world_map_pos"][1]))

            self.storage.add_component(self.player.metadata.entity_id, MapPosition3D(position["map_pos"][0],
                                                                                     position["map_pos"][1],
                                                                                     position["map_pos"][2]))

            self.storage.add_component(self.player.metadata.entity_id, SuperChunkPosition2D(position["superchunk_pos"][0],
                                                                                            position["superchunk_pos"][1]))

            self.storage.add_component(self.player.metadata.entity_id, ChunkPosition2D(position["chunk_pos"][0],
                                                                                       position["chunk_pos"][1]))

        else:
            pass

        worldmap_pos = self.storage.component_for_entity(self.player.metadata.entity_id, WorldMapPosition2D)
        wcameraX1 = worldmap_pos.x - 29
        wcameraX2 = worldmap_pos.x + 31
        wcameraY1 = worldmap_pos.y - 19
        wcameraY2 = worldmap_pos.y + 21

        self.world_map = WorldMap(self.storage, 64, 64, settings.WORLD_MAP, 3, 3, 8, 8, [8675309])
        self.world_map_camera = AsciiCamera(self.storage, wcameraX1, wcameraY1, wcameraX2, wcameraY2, self.console["game_world"],
                                            0, 0, 60, 60, 0, 0, 0, tags=["worldmap"])

        map_pos = self.storage.component_for_entity(self.player.metadata.entity_id, MapPosition3D)
        mcameraX1 = map_pos.x - 29
        mcameraX2 = map_pos.x + 31
        mcameraY1 = map_pos.z - 19
        mcameraY2 = map_pos.z + 21
        self.local_map_camera = AsciiCamera(self.storage, mcameraX1, mcameraY1, mcameraX2, mcameraY2, self.console["game_world"],
                                            0, 0, 60, 60, 0, 0, 0, tags=["localmap"])

        self.world_map_camera_processor = WorldMapCameraProcessor()
        self.local_map_camera_processor = LocalMapCameraProcessor()
        self.ct_processor = CTProcessor()
        self.storage.add_processor(self.ct_processor, 1)
        self.storage.add_processor(self.world_map_camera_processor, 0)
        self.storage.add_processor(self.local_map_camera_processor, 0)
        self.game_menu = GameMenu(self.console["game_world"], "menu", 60)
        self.message_log = MessageLog(self.console["game_world"], 0, 40, 59, 10, "/ Message log /")

        for filename in os.listdir(settings.MAP_DIR):
            if filename.endswith(".json"):
                file = settings.MAP_DIR + "/" + filename
                with open(file) as f:
                    staticmap = json.load(f)
                    self.static_map.append(staticmap)

        sc_posX = position["world_map_pos"][0]
        sc_posY = position["world_map_pos"][1]
        c_posX = position["superchunk_pos"][0]
        c_posY = position["superchunk_pos"][1]
        m_posX = position["chunk_pos"][0]
        m_posY = position["chunk_pos"][1]

        chunk_area = self.storage.component_for_entity(self.world_map.metadata.entity_id, ChunkArea2D)
        chunk = Chunk2D(self.storage, position["superchunk_pos"][0], position["superchunk_pos"][1], chunk_area.width,
                        chunk_area.height, position["chunk_pos"][0], position["chunk_pos"][1])
        map_conf = [m for m in self.static_map if m["name"] == position["start_map"]]
        map_conf = map_conf[0]
        map_file = settings.MAP_DIR + "/" + map_conf["file"]
        start_map = Map3D(self.storage, 128, 64, 128, m_posX, m_posY, constants.SEA_LEVEL, map_file)
        chunk.metadata.containers["loaded_maps"][m_posX][m_posY] = start_map.metadata
        superchunk = self.world_map.metadata.containers["superchunks"][sc_posX][sc_posY]
        superchunk.containers["loaded_chunks"][c_posX][c_posY] = chunk.metadata

        self.gwk = GameWorldKernel({}, 0, self.player, self.world_map, superchunk, chunk.metadata, start_map.metadata,
                                   self.world_map_camera, self.local_map_camera, self)

        self.uik = UIKernel({}, 0, self.message_log, self.game_menu)
        self.state_change("ct_await")

    def enter_scene(self):
        pass

    def exit_scene(self):
        pass

    def destroy(self):
        pass

    def handle_input_map(self, input_map, key, action_queue):
        for k, v in input_map.user.items():
            if key.vk == v.keycode and key.c == ord(v.char) and key.lalt == v.lalt and key.lctrl == v.lctrl \
                    and key.lmeta == v.lmeta and key.rctrl == v.rctrl and key.ralt == v.ralt and key.rmeta == v.rmeta \
                    and key.shift == v.shift:
                action_queue.append(k)
                break

        for k, v in input_map.default.items():
            if key.vk == v.keycode and key.c == ord(v.char) and key.lalt == v.lalt and key.lctrl == v.lctrl \
                    and key.lmeta == v.lmeta and key.rctrl == v.rctrl and key.ralt == v.ralt and key.rmeta == v.rmeta \
                    and key.shift == v.shift:
                action_queue.append(k)
                break

    def handle_input(self, key):
        if self.state == "world_map":
            self.handle_input_map(self.input_map, key, self.input_action_queue["world_map"])
        elif self.state == "local_map":
            self.handle_input_map(self.input_map, key, self.input_action_queue["local_map"])
        elif self.state == "player_at":
            self.handle_input_map(self.input_map, key, self.input_action_queue["player_at"])


    def update(self, dt):

        if self.state == "ct_await":
            player_state = self.gwk.player_state
            if player_state == "local_map":
                self.local_render = True
            else:
                self.local_render = False

        elif self.state == "player_at":
            player_state = self.gwk.syscall("get_player_state")
            if player_state == "local_map":
                self.local_render = True
                if len(self.input_action_queue["player_at"]) > 0:
                    if self.input_action_queue["player_at"][-1] == "camera_center_move_east" or \
                            self.input_action_queue["player_at"][-1] == "camera_center_move_east_alt":
                        self.input_action_queue["player_at"].pop()
                        self.gwk.syscall("move_local", direction="east")

                    elif self.input_action_queue["player_at"][-1] == "camera_center_move_west" or \
                            self.input_action_queue["player_at"][-1] == "camera_center_move_west_alt":
                        self.input_action_queue["player_at"].pop()
                        self.gwk.syscall("move_local", direction="west")

                    elif self.input_action_queue["player_at"][-1] == "camera_center_move_north" or \
                            self.input_action_queue["player_at"][-1] == "camera_center_move_north_alt":
                        self.input_action_queue["player_at"].pop()
                        self.gwk.syscall("move_local", direction="north")

                    elif self.input_action_queue["player_at"][-1] == "camera_center_move_south" or \
                            self.input_action_queue["player_at"][-1] == "camera_center_move_south_alt":
                        self.input_action_queue["player_at"].pop()
                        self.gwk.syscall("move_local", direction="south")

                    elif self.input_action_queue["player_at"][-1] == "camera_center_move_northwest" or \
                            self.input_action_queue["player_at"][-1] == "camera_center_move_northwest_alt":
                        self.input_action_queue["player_at"].pop()
                        self.gwk.syscall("move_local", direction="northwest")

                    elif self.input_action_queue["player_at"][-1] == "camera_center_move_northeast" or \
                            self.input_action_queue["player_at"][-1] == "camera_center_move_northeast_alt":
                        self.input_action_queue["player_at"].pop()
                        self.gwk.syscall("move_local", direction="northeast")

                    elif self.input_action_queue["player_at"][-1] == "camera_center_move_southwest" or \
                            self.input_action_queue["player_at"][-1] == "camera_center_move_southwest_alt":
                        self.input_action_queue["player_at"].pop()
                        self.gwk.syscall("move_local", direction="southwest")

                    elif self.input_action_queue["player_at"][-1] == "camera_center_move_southeast" or \
                            self.input_action_queue["player_at"][-1] == "camera_center_move_southeast_alt":
                        self.input_action_queue["player_at"].pop()
                        self.gwk.syscall("move_local", direction="southeast")
                player = self.gwk.player.metadata
                actor = self.storage.component_for_entity(player.entity_id, Actor)
                if actor.ct < 100:
                    self.state_change("ct_await")
            else:
                self.local_render = False

        elif self.state == "npc_at":
            a = self.gwk.syscall("get_at")
            actor = self.storage.component_for_entity(a.entity_id, Actor)
            if actor.ct < 100:
                self.state_change("ct_await")

        elif self.state == "world_map":
            self.local_render = False
            if len(self.input_action_queue["world_map"]) > 0:
                if self.input_action_queue["world_map"][-1] == "camera_center_move_east" or \
                        self.input_action_queue["world_map"][-1] == "camera_center_move_east_alt":
                    self.input_action_queue["world_map"].pop()
                    viewport = self.storage.component_for_entity(self.world_map_camera.metadata.entity_id, Rectangle)
                    worldmap_pos = self.storage.component_for_entity(self.player.metadata.entity_id, WorldMapPosition2D)
                    worldmap_area = self.storage.component_for_entity(self.world_map.metadata.entity_id, Area2D)
                    self.graphics_dirty = camera_center_move_east(viewport, worldmap_pos, worldmap_area)

                elif self.input_action_queue["world_map"][-1] == "camera_center_move_west" or \
                        self.input_action_queue["world_map"][-1] == "camera_center_move_west_alt":
                    self.input_action_queue["world_map"].pop()
                    viewport = self.storage.component_for_entity(self.world_map_camera.metadata.entity_id, Rectangle)
                    worldmap_pos = self.storage.component_for_entity(self.player.metadata.entity_id, WorldMapPosition2D)
                    self.graphics_dirty = camera_center_move_west(viewport, worldmap_pos)

                elif self.input_action_queue["world_map"][-1] == "camera_center_move_north" or \
                        self.input_action_queue["world_map"][-1] == "camera_center_move_north_alt":
                    self.input_action_queue["world_map"].pop()
                    viewport = self.storage.component_for_entity(self.world_map_camera.metadata.entity_id, Rectangle)
                    worldmap_pos = self.storage.component_for_entity(self.player.metadata.entity_id, WorldMapPosition2D)
                    self.graphics_dirty = camera_center_move_north(viewport, worldmap_pos)

                elif self.input_action_queue["world_map"][-1] == "camera_center_move_south" or\
                        self.input_action_queue["world_map"][-1] == "camera_center_move_south_alt":
                    self.input_action_queue["world_map"].pop()
                    viewport = self.storage.component_for_entity(self.world_map_camera.metadata.entity_id, Rectangle)
                    worldmap_pos = self.storage.component_for_entity(self.player.metadata.entity_id, WorldMapPosition2D)
                    worldmap_area = self.storage.component_for_entity(self.world_map.metadata.entity_id, Area2D)
                    self.graphics_dirty = camera_center_move_south(viewport, worldmap_pos, worldmap_area)

                elif self.input_action_queue["world_map"][-1] == "camera_center_move_northwest" or \
                        self.input_action_queue["world_map"][-1] == "camera_center_move_northwest_alt":
                    self.input_action_queue["world_map"].pop()
                    viewport = self.storage.component_for_entity(self.world_map_camera.metadata.entity_id, Rectangle)
                    worldmap_pos = self.storage.component_for_entity(self.player.metadata.entity_id, WorldMapPosition2D)
                    self.graphics_dirty = camera_center_move_northwest(viewport, worldmap_pos)

                elif self.input_action_queue["world_map"][-1] == "camera_center_move_northeast" or \
                        self.input_action_queue["world_map"][-1] == "camera_center_move_northeast_alt":
                    self.input_action_queue["world_map"].pop()
                    viewport = self.storage.component_for_entity(self.world_map_camera.metadata.entity_id, Rectangle)
                    worldmap_pos = self.storage.component_for_entity(self.player.metadata.entity_id, WorldMapPosition2D)
                    worldmap_area = self.storage.component_for_entity(self.world_map.metadata.entity_id, Area2D)
                    self.graphics_dirty = camera_center_move_northeast(viewport, worldmap_pos, worldmap_area)

                elif self.input_action_queue["world_map"][-1] == "camera_center_move_southwest" or \
                        self.input_action_queue["world_map"][-1] == "camera_center_move_southwest_alt":
                    self.input_action_queue["world_map"].pop()
                    viewport = self.storage.component_for_entity(self.world_map_camera.metadata.entity_id, Rectangle)
                    worldmap_pos = self.storage.component_for_entity(self.player.metadata.entity_id, WorldMapPosition2D)
                    worldmap_area = self.storage.component_for_entity(self.world_map.metadata.entity_id, Area2D)
                    self.graphics_dirty = camera_center_move_southwest(viewport, worldmap_pos, worldmap_area)

                elif self.input_action_queue["world_map"][-1] == "camera_center_move_southeast" or \
                        self.input_action_queue["world_map"][-1] == "camera_center_move_southeast_alt":
                    self.input_action_queue["world_map"].pop()
                    viewport = self.storage.component_for_entity(self.world_map_camera.metadata.entity_id, Rectangle)
                    worldmap_pos = self.storage.component_for_entity(self.player.metadata.entity_id, WorldMapPosition2D)
                    worldmap_area = self.storage.component_for_entity(self.world_map.metadata.entity_id, Area2D)
                    self.graphics_dirty = camera_center_move_southeast(viewport, worldmap_pos, worldmap_area)

        self.storage.process(render=False, dirty=self.graphics_dirty, local_render=self.local_render, gwk=self.gwk,
                             uik=self.uik)

    def draw(self):
        self.storage.process(render=True, dirty=self.graphics_dirty, local_render=self.local_render, gwk=self.gwk,
                             uik=self.uik)
        self.graphics_dirty = False
        self.game_menu.draw_window()
        self.message_log.draw_window()
        self.message_log.draw_messages()
        tcod.console_blit(self.console["game_world"], 0, 0, settings.CONSOLE_WIDTH, settings.CONSOLE_HEIGHT, 0, 0, 0)
        tcod.console_flush()