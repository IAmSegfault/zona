import tcod
import os
import threading
import time
import settings
import shelve
from game.scene import Scene
from gui.menu import MainMenu, SettingsMenu, ConfirmationMenu, SelectionMenu
from game.util.fs import savefile_exists
from os.path import isfile


class TitleScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.console["main_menu"] = tcod.console_new(settings.CONSOLE_WIDTH, settings.CONSOLE_HEIGHT)
        self.console["settings"] = tcod.console_new(settings.CONSOLE_WIDTH, settings.CONSOLE_HEIGHT)
        self.main_menu = MainMenu(self.console["main_menu"])
        self.settings_menu = SettingsMenu(self.console["settings"])
        self.charset_confirmation_lock = threading.Lock()
        self.charset_confirmation_countdown = 10
        self.revert_to_default_charset = False
        self.charset_options = []
        for file in os.listdir(settings.CHARSET_USER_DIR):
            if file.endswith(".png"):
                self.charset_options.append(file)
        self.charset_options.sort(reverse=True)
        self.charset_options.insert(0, "Default")
        self.charset_options.append("Back")
        self.font = False

        self.charset_select_menu = SelectionMenu(self.console["settings"], self.charset_options,
                                                 20, 20, 60, 30, title="Select a character set")

        self.delete_save_confirmation = ConfirmationMenu(self.console["settings"], "Are you sure [y/n?]", 20, 20, 60, 30,
                                                         "/ Confirm deletion /", bg_color=tcod.black, title_color=tcod.red)

        charset_confirmation_msg = "Reverting in 10 seconds, keep current character set [y/n]?"
        charset_confirmation_w = len(charset_confirmation_msg) + 4
        self.charset_confirmation = ConfirmationMenu(self.console["settings"], charset_confirmation_msg,
                                                     7, 20, charset_confirmation_w + 7, 30, "/ Confirm character set /")
        self.is_exit = False

    def revert_charset(self):
        while self.charset_confirmation_countdown > 0:

            self.charset_confirmation_lock.acquire()
            self.charset_confirmation_countdown -= 1
            self.charset_confirmation_lock.release()
            time.sleep(1)

        self.charset_confirmation_lock.acquire()
        if self.revert_to_default_charset is True:
            if self.state == "charset_confirmation":
                self.input_action_queue["charset_confirmation"].append("revert_charset")
        self.charset_confirmation_lock.release()


    def state_change(self, state):
        self.prev_state = self.state
        self.state = state
        for key, c in self.console.items():
            c.clear()

        if self.state == "charset_confirmation":
            self.charset_confirmation_lock.acquire()
            self.charset_confirmation_countdown = 10
            self.revert_to_default_charset = True
            self.charset_confirmation_lock.release()
            job = threading.Thread(target=self.revert_charset)
            job.start()

        if self.state == "settings":
            if self.revert_to_default_charset is True:
                self.revert_to_default_charset = False
                font = None
                config_file = settings.PERSISTENT_STORAGE + ".db"
                fullscreen = tcod.console_is_fullscreen()
                use_mouse = tcod.mouse_is_cursor_visible()
                if isfile(config_file):
                    config = shelve.open(settings.PERSISTENT_STORAGE, writeback=True)
                    if config["settings"]["prev_font"]:
                        font = config["settings"]["prev_font"]
                        config["settings"]["font"] = config["settings"]["prev_font"]
                        config["settings"]["prev_font"] = False
                    else:
                        font = settings.CP437

                    fullscreen = config["settings"]["fullscreen"]
                    use_mouse = config["settings"]["use_mouse"]
                    config.close()
                font_flags = tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_ASCII_INROW
                tcod.console_set_custom_font(font, font_flags)
                tcod.console_init_root(80, 50, settings.WINDOW_TITLE, False)
                tcod.console_set_fullscreen(fullscreen)
                tcod.mouse_show_cursor(use_mouse)
            else:
                config_file = settings.PERSISTENT_STORAGE + ".db"
                if isfile(config_file):
                    config = shelve.open(settings.PERSISTENT_STORAGE, writeback=True)
                    config["settings"]["font"] = self.font
                    config.close()

    def handle_input(self, key):
        if self.state == "menu_select":
            if key.vk == tcod.KEY_UP and key.pressed:
                self.input_action_queue["menu_select"].append("cursor_up")
            elif key.vk == tcod.KEY_DOWN and key.pressed:
                self.input_action_queue["menu_select"].append("cursor_down")
            elif key.vk == tcod.KEY_ENTER and key.pressed:
                self.input_action_queue["menu_select"].append("select")

        elif self.state == "settings":
            if key.vk == tcod.KEY_DOWN and key.pressed:
                self.input_action_queue["settings_menu"].append("cursor_down")
            elif key.vk == tcod.KEY_UP and key.pressed:
                self.input_action_queue["settings_menu"].append("cursor_up")
            elif key.vk == tcod.KEY_ENTER and key.pressed:
                self.input_action_queue["settings_menu"].append("select")

        elif self.state == "delete_confirmation":
            if key.vk == tcod.KEY_CHAR and key.pressed:
                if key.c == ord('y'):
                    self.input_action_queue["delete_confirmation"].append("close_confirmation")
                    self.input_action_queue["delete_confirmation"].append("delete_save")
                elif key.c == ord('n'):
                    self.input_action_queue["delete_confirmation"].append("close_confirmation")

        elif self.state == "charset_select":
            if key.vk == tcod.KEY_DOWN and key.pressed:
                self.input_action_queue["charset_select"].append("cursor_down")
            elif key.vk == tcod.KEY_UP and key.pressed:
                self.input_action_queue["charset_select"].append("cursor_up")
            elif key.vk == tcod.KEY_ENTER and key.pressed:
                self.input_action_queue["charset_select"].append("select")

        elif self.state == "charset_confirmation":
            if key.vk == tcod.KEY_CHAR and key.pressed:
                if key.c == ord('y'):
                    self.input_action_queue["charset_confirmation"].append("keep_charset")
                elif key.c == ord('n'):
                    self.input_action_queue["charset_confirmation"].append("revert_charset")

        return self.is_exit

    def init_scene(self):
        self.state = "menu_select"
        self.input_action_queue["menu_select"] = []
        self.input_action_queue["settings_menu"] = []
        self.input_action_queue["delete_confirmation"] = []
        self.input_action_queue["charset_confirmation"] = []
        self.input_action_queue["charset_select"] = []

    def enter_scene(self):
        self.main_menu.menu_select = "new game"
        self.main_menu.cursorposY = 20
        self.main_menu.continue_muted = not savefile_exists()

    def destroy(self):
        pass

    def exit_scene(self):
        tcod.console_clear(0)

    def update(self, dt):

        if self.state == "menu_select":
            self.main_menu.continue_muted = not savefile_exists()
            if len(self.input_action_queue["menu_select"]) > 0:
                if self.input_action_queue["menu_select"][-1] == "cursor_down":
                    self.input_action_queue["menu_select"].pop()
                    self.main_menu.cursor_down()

                elif self.input_action_queue["menu_select"][-1] == "cursor_up":
                    self.input_action_queue["menu_select"].pop()
                    self.main_menu.cursor_up()

                elif self.input_action_queue["menu_select"][-1] == "select":
                    selection = self.main_menu.menu_select
                    self.input_action_queue["menu_select"].pop()

                    if selection == "new game":
                        self.manager.set_scene("chargen")

                    elif selection == "settings":
                        self.state_change("settings")

                    elif selection == "exit":
                        self.is_exit = True

        elif self.state == "settings":
            self.settings_menu.delete_save_muted = not savefile_exists()
            if len(self.input_action_queue["settings_menu"]) > 0:
                if self.input_action_queue["settings_menu"][-1] == "cursor_down":
                    self.input_action_queue["settings_menu"].pop()
                    self.settings_menu.cursor_down()

                elif self.input_action_queue["settings_menu"][-1] == "cursor_up":
                    self.input_action_queue["settings_menu"].pop()
                    self.settings_menu.cursor_up()

                elif self.input_action_queue["settings_menu"][-1] == "select":
                    self.input_action_queue["settings_menu"].pop()
                    if self.settings_menu.menu_select == "delete_save_file" and not self.settings_menu.delete_save_muted:
                        self.state_change("delete_confirmation")

                    elif self.settings_menu.menu_select == "set_character_map":
                        self.state_change("charset_select")

                    elif self.settings_menu.menu_select == "back":
                        self.settings_menu.menu_select = "delete_save_file"
                        self.settings_menu.cursorposY = 4
                        self.state_change("menu_select")

        elif self.state == "delete_confirmation":
            if len(self.input_action_queue["delete_confirmation"]) > 0:
                if self.input_action_queue["delete_confirmation"][-1] == "delete_save":
                    self.input_action_queue["delete_confirmation"].pop()
                    self.settings_menu.delete_save_file()

                elif self.input_action_queue["delete_confirmation"][-1] == "close_confirmation":
                    self.input_action_queue["delete_confirmation"].pop()
                    self.state_change("settings")

        elif self.state == "charset_select":
            if len(self.input_action_queue["charset_select"]) > 0:
                if self.input_action_queue["charset_select"][-1] == "cursor_down":
                    self.input_action_queue["charset_select"].pop()
                    self.charset_select_menu.cursor_down()

                elif self.input_action_queue["charset_select"][-1] == "cursor_up":
                    self.input_action_queue["charset_select"].pop()
                    self.charset_select_menu.cursor_up()

                elif self.input_action_queue["charset_select"][-1] == "select":
                    self.input_action_queue["charset_select"].pop()
                    if self.charset_select_menu.selections[self.charset_select_menu.menu_select] == "Back":
                        self.charset_select_menu.selection_start = 0
                        self.charset_select_menu.selection_end = 4
                        if self.charset_select_menu.selection_count < self.charset_select_menu.selection_end:
                            self.charset_select_menu.selection_end = self.charset_select_menu.selection_count
                        self.charset_select_menu.menu_select = 0
                        self.charset_select_menu.cursorposY = self.charset_select_menu.y + 2
                        self.charset_select_menu.logical_position = 0
                        self.state_change("settings")
                    elif self.charset_select_menu.selections[self.charset_select_menu.menu_select] == "Default":
                        font = settings.CP437
                        font_flags = tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_ASCII_INROW
                        tcod.console_set_custom_font(font, font_flags)
                        tcod.console_init_root(80, 50, settings.WINDOW_TITLE, False)
                        config_file = settings.PERSISTENT_STORAGE + ".db"
                        if isfile(config_file):
                            config = shelve.open(settings.PERSISTENT_STORAGE, writeback=True)
                            config["settings"]["font"] = False
                            config["settings"]["prev_font"] = False
                            fullscreen = config["settings"]["fullscreen"]
                            use_mouse = config["settings"]["use_mouse"]
                            config.close()
                            tcod.console_set_fullscreen(fullscreen)
                            tcod.mouse_show_cursor(use_mouse)
                        self.state_change("settings")
                    else:
                        font = settings.CHARSET_USER_DIR + "/" + self.charset_select_menu.selections[self.charset_select_menu.menu_select]
                        font_flags = tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_ASCII_INROW
                        tcod.console_set_custom_font(font, font_flags)
                        tcod.console_init_root(80, 50, settings.WINDOW_TITLE, False)
                        config_file = settings.PERSISTENT_STORAGE + ".db"
                        if isfile(config_file):
                            config = shelve.open(settings.PERSISTENT_STORAGE, writeback=True)
                            fullscreen = config["settings"]["fullscreen"]
                            use_mouse = config["settings"]["use_mouse"]
                            if config["settings"]["font"]:
                                if config["settings"]["prev_font"]:
                                    if config["settings"]["prev_font"] != config["settings"]["font"]:
                                        config["settings"]["prev_font"] = config["settings"]["font"]
                            self.font = font
                            config.close()
                            tcod.console_set_fullscreen(fullscreen)
                            tcod.mouse_show_cursor(use_mouse)
                        self.state_change("charset_confirmation")

        elif self.state == "charset_confirmation":
            if len(self.input_action_queue["charset_confirmation"]) > 0:
                if self.input_action_queue["charset_confirmation"][-1] == "keep_charset":
                    self.input_action_queue["charset_confirmation"].pop()
                    self.charset_confirmation_lock.acquire()
                    self.revert_to_default_charset = False
                    self.charset_confirmation_countdown = 0
                    self.state_change("settings")
                    self.charset_confirmation_lock.release()
                elif self.input_action_queue["charset_confirmation"][-1] == "revert_charset":
                    self.input_action_queue["charset_confirmation"].pop()
                    self.charset_confirmation_lock.acquire()
                    self.charset_confirmation_countdown = 0
                    self.state_change("settings")
                    self.charset_confirmation_lock.release()

    def draw(self):
        if self.state == "menu_select":
            self.main_menu.draw_title()
            self.main_menu.draw_cursor()
            self.main_menu.draw_options()
            tcod.console_blit(self.console["main_menu"], 0, 0, settings.CONSOLE_WIDTH, settings.CONSOLE_HEIGHT, 0, 0, 0)

        elif self.state == "settings":
            self.settings_menu.draw_cursor()
            self.settings_menu.draw_checkbox()
            self.settings_menu.draw_options()
            tcod.console_blit(self.console["settings"], 0, 0, settings.CONSOLE_WIDTH, settings.CONSOLE_HEIGHT, 0, 0, 0)

        elif self.state == "delete_confirmation":
            self.settings_menu.draw_checkbox()
            self.settings_menu.draw_options()
            self.delete_save_confirmation.draw_confirmation()
            tcod.console_blit(self.console["settings"], 0, 0, settings.CONSOLE_WIDTH, settings.CONSOLE_HEIGHT, 0, 0, 0)

        elif self.state == "charset_select":
            self.settings_menu.draw_checkbox()
            self.settings_menu.draw_options()
            self.charset_select_menu.draw_window()
            self.charset_select_menu.draw_cursor()
            self.charset_select_menu.draw_options()
            tcod.console_blit(self.console["settings"], 0, 0, settings.CONSOLE_WIDTH, settings.CONSOLE_HEIGHT, 0, 0, 0)

        elif self.state == "charset_confirmation":
            self.settings_menu.draw_checkbox()
            self.settings_menu.draw_options()
            self.charset_confirmation.draw_confirmation()
            tcod.console_blit(self.console["settings"], 0, 0, settings.CONSOLE_WIDTH, settings.CONSOLE_HEIGHT, 0, 0, 0)

        tcod.console_flush()