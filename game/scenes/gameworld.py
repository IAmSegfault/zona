import json
import settings
import tcod
import json
import logging
from os.path import isfile
from game.scene import Scene
from ecs.entities.worldmap import WorldMap
from ecs.entities.camera import AsciiCamera
from ecs.entities.player import PlayerCharacter
from ecs.components.position import WorldMapPosition2D, SuperChunkPosition2D, ChunkPosition2D, MapPosition3D
from ecs.systems.mapdraw import WorldMapCameraProcessor
from ecs.components.dimension import Rectangle, Area2D
from ecs.entities.camera import world_to_camera_pos
from game.util.input import InputMap
from game.util.camera import *
from gui.menu import GameMenu, MessageLog


class GameWorldScene(Scene):

    def __init__(self, manager):
        super().__init__(manager)
        self.console["game_world"] = tcod.console_new(settings.CONSOLE_WIDTH, settings.CONSOLE_HEIGHT)
        self.input_action_queue = {}
        self.input_action_queue["init"] = []
        self.input_action_queue["world_map"] = []
        self.input_action_queue["map"] = []
        self.state = "init"
        self.world_map = None
        self.world_map_camera = None
        self.world_map_camera_processor = None
        self.game_menu = None
        self.message_log = None
        self.player = None
        self.graphics_dirty = True
        self.input_map = None

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
        else:
            pass

        worldmap_pos = self.storage.component_for_entity(self.player.metadata.entity_id, WorldMapPosition2D)
        cameraX1 = worldmap_pos.x - 29
        cameraX2 = worldmap_pos.x + 31
        cameraY1 = worldmap_pos.y - 19
        cameraY2 = worldmap_pos.y + 21

        self.world_map = WorldMap(self.storage, 64, 64, settings.WORLD_MAP, 3, 3, 8, 8, [8675309])
        self.world_map_camera = AsciiCamera(self.storage, cameraX1, cameraY1, cameraX2, cameraY2, self.console["game_world"],
                                            0, 0, 60, 60, 0, 0, 0)
        self.world_map_camera_processor = WorldMapCameraProcessor()
        self.storage.add_processor(self.world_map_camera_processor, 0)
        self.game_menu = GameMenu(self.console["game_world"], "menu", 60)
        self.message_log = MessageLog(self.console["game_world"], 0, 40, 59, 10, "/ Message log /")
        self.state_change("world_map")

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
        elif self.state == "map":
            self.handle_input_map(self.input_map, key, self.input_action_queue["map"])

    def update(self, dt):
        if self.state == "world_map":
            if len(self.input_action_queue["world_map"]) > 0:
                if self.input_action_queue["world_map"][-1] == "camera_center_move_east":
                    self.input_action_queue["world_map"].pop()
                    viewport = self.storage.component_for_entity(self.world_map_camera.metadata.entity_id, Rectangle)
                    worldmap_pos = self.storage.component_for_entity(self.player.metadata.entity_id, WorldMapPosition2D)
                    worldmap_area = self.storage.component_for_entity(self.world_map.metadata.entity_id, Area2D)
                    self.graphics_dirty = camera_center_move_east(viewport, worldmap_pos, worldmap_area)

                elif self.input_action_queue["world_map"][-1] == "camera_center_move_west":
                    self.input_action_queue["world_map"].pop()
                    viewport = self.storage.component_for_entity(self.world_map_camera.metadata.entity_id, Rectangle)
                    worldmap_pos = self.storage.component_for_entity(self.player.metadata.entity_id, WorldMapPosition2D)
                    self.graphics_dirty = camera_center_move_west(viewport, worldmap_pos)

                elif self.input_action_queue["world_map"][-1] == "camera_center_move_north":
                    self.input_action_queue["world_map"].pop()
                    viewport = self.storage.component_for_entity(self.world_map_camera.metadata.entity_id, Rectangle)
                    worldmap_pos = self.storage.component_for_entity(self.player.metadata.entity_id, WorldMapPosition2D)
                    self.graphics_dirty = camera_center_move_north(viewport, worldmap_pos)

                elif self.input_action_queue["world_map"][-1] == "camera_center_move_south":
                    self.input_action_queue["world_map"].pop()
                    viewport = self.storage.component_for_entity(self.world_map_camera.metadata.entity_id, Rectangle)
                    worldmap_pos = self.storage.component_for_entity(self.player.metadata.entity_id, WorldMapPosition2D)
                    worldmap_area = self.storage.component_for_entity(self.world_map.metadata.entity_id, Area2D)
                    self.graphics_dirty = camera_center_move_south(viewport, worldmap_pos, worldmap_area)

                elif self.input_action_queue["world_map"][-1] == "camera_center_move_northwest":
                    self.input_action_queue["world_map"].pop()
                    viewport = self.storage.component_for_entity(self.world_map_camera.metadata.entity_id, Rectangle)
                    worldmap_pos = self.storage.component_for_entity(self.player.metadata.entity_id, WorldMapPosition2D)
                    self.graphics_dirty = camera_center_move_northwest(viewport, worldmap_pos)

                elif self.input_action_queue["world_map"][-1] == "camera_center_move_northeast":
                    self.input_action_queue["world_map"].pop()
                    viewport = self.storage.component_for_entity(self.world_map_camera.metadata.entity_id, Rectangle)
                    worldmap_pos = self.storage.component_for_entity(self.player.metadata.entity_id, WorldMapPosition2D)
                    worldmap_area = self.storage.component_for_entity(self.world_map.metadata.entity_id, Area2D)
                    self.graphics_dirty = camera_center_move_northeast(viewport, worldmap_pos, worldmap_area)

                elif self.input_action_queue["world_map"][-1] == "camera_center_move_southwest":
                    self.input_action_queue["world_map"].pop()
                    viewport = self.storage.component_for_entity(self.world_map_camera.metadata.entity_id, Rectangle)
                    worldmap_pos = self.storage.component_for_entity(self.player.metadata.entity_id, WorldMapPosition2D)
                    worldmap_area = self.storage.component_for_entity(self.world_map.metadata.entity_id, Area2D)
                    self.graphics_dirty = camera_center_move_southwest(viewport, worldmap_pos, worldmap_area)

                elif self.input_action_queue["world_map"][-1] == "camera_center_move_southeast":
                    self.input_action_queue["world_map"].pop()
                    viewport = self.storage.component_for_entity(self.world_map_camera.metadata.entity_id, Rectangle)
                    worldmap_pos = self.storage.component_for_entity(self.player.metadata.entity_id, WorldMapPosition2D)
                    worldmap_area = self.storage.component_for_entity(self.world_map.metadata.entity_id, Area2D)
                    self.graphics_dirty = camera_center_move_southeast(viewport, worldmap_pos, worldmap_area)

    def draw(self):
        self.storage.process(True, self.graphics_dirty)
        self.graphics_dirty = False
        self.game_menu.draw_window()
        self.message_log.draw_window()
        self.message_log.draw_messages()
        tcod.console_blit(self.console["game_world"], 0, 0, settings.CONSOLE_WIDTH, settings.CONSOLE_HEIGHT, 0, 0, 0)
        tcod.console_flush()