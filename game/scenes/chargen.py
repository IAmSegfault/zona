import tcod
import json
import os
import settings
from os.path import isdir, isfile
from os import makedirs
from game.scene import Scene
from game.util.constants import Palette
from game.util.text import DocumentWrapper
from game.util.dice import d6
from gui.menu import InputMenu, ConfirmationMenu, GameMenu, SelectionMenu, StatSelect

class CharGenScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)

        self.char_classes = {}
        self.class_list = []
        self.character = {}
        self.stats = {}
        self.initialize_character()
        self.initialize_stats()
        self.stat_roll = []
        self.console["chargen"] = tcod.console_new(settings.CONSOLE_WIDTH, settings.CONSOLE_HEIGHT)
        self.input_action_queue = {}
        self.name_input = InputMenu(self.console["chargen"], 10, 20, 50, 28, title="/ What is your name? /",
                                    message="Enter a first name:")

        self.random_prompt = ConfirmationMenu(self.console["chargen"], "Would you like a character randomly made for you [y/n]?",
                                              10, 20, 50, 25, "/ Auto create character /")

        self.game_menu = GameMenu(self.console["chargen"], "init", 60, Palette.WHITE.value, Palette.GREEN.value)

        self.class_selection_menu = None
        self.roll_lock = False

        self.stat_selection_menu = None
        self.stats = []
    def initialize_stats(self):
        self.stats = {"str": 0, "dex": 0, "con": 0, "int": 0, "wis": 0, "cha": 0}

    def initialize_character(self):
        self.character["name"] = ""
        self.character["classname"] = ""
        self.character["stats"] = []
        self.character["slots"] = []
        self.character["groups"] = []
        self.character["raises"] = []
        self.character["level"] = 1
        self.character["xp"] = 0
        self.character["hit_dice"] = 1
        self.character["hit_dice_type"] = 6
        self.character["hit_dice_modifier"] = 0
        self.character["max_hit_points"] = 0
        self.character["attack_value"] = 0
        self.character["saving_throw"] = 0
        self.character["xp"] = 0
        self.character["xp_progression"] = []
        self.character["attack_value_progression"] = []
        self.character["saving_throw_progression"] = []
        self.character["slot_progression"] = []
        self.character["group_progression"] = []
        self.character["hit_dice_progression"] = []

    def state_change(self, state):
        self.prev_state = self.state
        self.state = state

        if self.prev_state == "random_prompt" and self.state == "class_select":
            self.game_menu.state = "class_description"

        if self.prev_state == "stat_select" and self.state == "class_select":
            self.game_menu.state = "class_description"
            self.initialize_character()
            self.stat_selection_menu.selections = []
            for i in range(len(self.stat_selection_menu.defaults)):
                self.stat_selection_menu.selections.append(list(self.stat_selection_menu.defaults[i]))

        if self.prev_state == "class_select" and self.state == "stat_select":
            self.game_menu.state = "stat_list"

            if not self.roll_lock:
                self.stats = []
                self.roll_lock = True
                for i in range(6):
                    roll = d6(3)
                    self.stats.append(roll)

            self.stat_selection_menu.set_stats(self.stats)


    def handle_input(self, key):
        if self.state == "random_prompt":
            if key.vk == tcod.KEY_CHAR:
                if key.c == ord("y"):
                    pass
                elif key.c == ord("n"):
                    self.input_action_queue["random_prompt"].append("player_create")
            elif key.vk == tcod.KEY_ESCAPE:
                self.input_action_queue["random_prompt"].append("back")

        elif self.state == "class_select":
            if key.vk == tcod.KEY_ESCAPE:
                self.input_action_queue["class_select"].append("back")
            elif key.vk == tcod.KEY_DOWN:
                self.input_action_queue["class_select"].append("down")
            elif key.vk == tcod.KEY_UP:
                self.input_action_queue["class_select"].append("up")
            elif key.vk == tcod.KEY_ENTER:
                self.input_action_queue["class_select"].append("select")

        elif self.state == "stat_select":
            self.stat_selection_menu.handle_input(key)
            if self.stat_selection_menu.backtrack:
                self.stat_selection_menu.backtrack = False
                self.input_action_queue["stat_select"].append("back")
            elif key.vk == tcod.KEY_DOWN:
                self.input_action_queue["stat_select"].append("cursor_down")
            elif key.vk == tcod.KEY_UP:
                self.input_action_queue["stat_select"].append("cursor_up")

        elif self.state == "name_input":
            self.name_input.handle_input(key)
            if key.vk == tcod.KEY_ESCAPE:
                self.input_action_queue["name_input"].append("back")

    def init_scene(self):
        self.state = "random_prompt"
        self.input_action_queue["random_prompt"] = []
        self.input_action_queue["class_select"] = []
        self.input_action_queue["stat_select"] = []

        class_dir = settings.DATA_DIR + "/playerclass"
        for file in os.listdir(class_dir):
            if file.endswith(".json"):
                filepath = class_dir + "/" + file
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    self.char_classes[data["classname"]] = data
        dw = DocumentWrapper(width=self.game_menu.w - 4)
        for cls, data in self.char_classes.items():
            self.class_list.append(cls)
            data["description"] = dw.wrap(data["description"])
        self.class_selection_menu = SelectionMenu(self.console["chargen"], self.class_list, 10, 20, 50, 28, "Select an archetype")
        self.stat_selection_menu = StatSelect(self.console["chargen"], [], 20, 20, 50, 33, "/ Assign your stats /")

    def enter_scene(self):
        pass

    def destroy(self):
        pass

    def exit_scene(self):
        self.state_change("random_prompt")
        self.roll_lock = False
        tcod.console_clear(0)

    def update(self, dt):
        if self.state == "random_prompt":
            if len(self.input_action_queue["random_prompt"]) > 0:
                if self.input_action_queue["random_prompt"][-1] == "player_create":
                    self.input_action_queue["random_prompt"].pop()
                    self.state_change("class_select")
                elif self.input_action_queue["random_prompt"][-1] == "random_create":
                    self.input_action_queue["random_prompt"].pop()
                    self.state_change("random_create")
                elif self.input_action_queue["random_prompt"][-1] == "back":
                    self.manager.set_scene("title")

        elif self.state == "class_select":
            if len(self.input_action_queue["class_select"]) > 0:
                if self.input_action_queue["class_select"][-1] == "back":
                    self.input_action_queue["class_select"].pop()
                    self.manager.set_scene("title")

                elif self.input_action_queue["class_select"][-1] == "down":
                    self.input_action_queue["class_select"].pop()
                    self.class_selection_menu.cursor_down()

                elif self.input_action_queue["class_select"][-1] == "up":
                    self.input_action_queue["class_select"].pop()
                    self.class_selection_menu.cursor_up()

                elif self.input_action_queue["class_select"][-1] == "select":
                    self.input_action_queue["class_select"].pop()
                    cls = self.char_classes[self.class_list[self.class_selection_menu.menu_select]]
                    self.character["classname"] = cls["classname"]
                    self.character["xp_progression"] = cls["attributes"]["xp"]
                    self.character["attack_value_progression"] = cls["attributes"]["av"]
                    self.character["saving_throw_progression"] = cls["attributes"]["st"]
                    self.character["slot_progression"] = cls["attributes"]["slots"]
                    self.character["group_progression"] = cls["attributes"]["groups"]
                    self.character["hit_dice_progression"] = cls["attributes"]["hitdice"]
                    self.character["attack_value"] = cls["attributes"]["av"][0]
                    self.character["saving_throw"] = cls["attributes"]["st"][0]
                    hd = cls["attributes"]["hitdice"][0]
                    hd = list(hd)
                    self.character["hit_dice"] = int(hd[0])
                    self.character["hit_dice_type"] = int(hd[2])
                    self.character["hit_dice_modifier"] = int(hd[4])
                    self.character["max_hit_points"] = (int(hd[0]) * int(hd[2])) + int(hd[4])
                    self.state_change("stat_select")

        elif self.state == "stat_select":
            if len(self.input_action_queue["stat_select"]) > 0:
                if self.input_action_queue["stat_select"][-1] == "back":
                    self.input_action_queue["stat_select"].pop()
                    self.state_change("class_select")

                elif self.input_action_queue["stat_select"][-1] == "cursor_down":
                    self.input_action_queue["stat_select"].pop()
                    self.stat_selection_menu.cursor_down()

                elif self.input_action_queue["stat_select"][-1] == "cursor_up":
                    self.input_action_queue["stat_select"].pop()
                    self.stat_selection_menu.cursor_up()

                elif self.input_action_queue["stat_select"][-1] == "cursor_up":
                    self.input_action_queue["stat_select"].pop()
                    self.stat_selection_menu.cursor_up()

            if not self.stat_selection_menu.selecting:
                self.stat_selection_menu.selecting = True
                self.character["stats"] = [self.stat_selection_menu.stats[selection[1]] for selection in self.stat_selection_menu.selections]
                self.state_change("name_input")

        elif self.state == "name_input":
            if not self.name_input.reading_input:
                text = "".join(self.name_input.input)
                if text == "":
                    self.name_input.reading_input = True
                else:
                    self.character["name"] = text
                    directive = {}
                    position = None
                    with open(settings.NEWGAME_POSITION) as f:
                        position = json.load(f)
                    directive["character"] = self.character
                    directive["init_mode"] = "new_game"
                    directive["position"] = position

                    if not isdir(settings.TEMP_DIR):
                        makedirs(settings.TEMP_DIR)
                    if isfile(settings.GAME_BOOTLOADER):
                        os.remove(settings.GAME_BOOTLOADER)

                    with open(settings.GAME_BOOTLOADER, 'w') as f:
                        json.dump(directive, f)

                    self.manager.set_scene("game_world")

    def draw(self):
        self.console["chargen"].clear()
        self.game_menu._draw_border()

        if self.state == "random_prompt":
            self.random_prompt.draw_confirmation()

        elif self.state == "class_select":
            self.class_selection_menu.draw_window()
            self.class_selection_menu.draw_cursor()
            self.class_selection_menu.draw_options()
            args = {"message": self.char_classes[self.class_list[self.class_selection_menu.menu_select]]["description"]}
            self.game_menu.draw_window(args=args)

        elif self.state == "name_input":
            self.name_input.draw_window()
            self.name_input.draw_input()
            self.name_input.draw_cursor()

        elif self.state == "stat_select":
            self.game_menu.draw_window(self.stat_selection_menu.stats)
            self.stat_selection_menu.draw_window()
            self.stat_selection_menu.draw_cursor()
            self.stat_selection_menu.draw_selections()

        tcod.console_blit(self.console["chargen"], 0, 0, settings.CONSOLE_WIDTH, settings.CONSOLE_HEIGHT, 0, 0, 0)
        tcod.console_flush()
