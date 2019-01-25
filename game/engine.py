import tcod
import settings
from os.path import isdir, isfile
import shutil
import shelve
import time
from os import makedirs
from game.scene import SceneManager
from game.scenes.title import TitleScene
from game.scenes.chargen import CharGenScene
from game.scenes.gameworld import GameWorldScene


class Engine(object):
    def __init__(self):
        self.config_file = settings.PERSISTENT_STORAGE + ".db"
        if not isfile(self.config_file):
            config = shelve.open(settings.PERSISTENT_STORAGE, writeback=True)
            config["settings"] = settings.STORAGE_SETTINGS
            config["version"] = settings.VERSION
            config.close()
        else:
            config = shelve.open(settings.PERSISTENT_STORAGE, writeback=True)
            if config["version"]["major"] < settings.VERSION["major"]:
                config["settings"] = settings.STORAGE_SETTINGS
                config["version"] = settings.VERSION
            config.close()

        config = shelve.open(settings.PERSISTENT_STORAGE, flag='r')
        self.limit_fps = config["settings"]["limit_fps"]
        self.screen_width = config["settings"]["screen_width"]
        self.screen_height = config["settings"]["screen_height"]
        self.fullscreen = config["settings"]["fullscreen"]
        self.use_mouse = config["settings"]["use_mouse"]
        self.tcod_font = config["settings"]["font"]
        config.close()

        if self.tcod_font:
            if isfile(self.tcod_font):
                self.font_path = self.tcod_font
            else:
                self.font_path = settings.CP437
        else:
            self.font_path = settings.CP437

        self.font_flags = tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_ASCII_INROW
        self.window_title = settings.WINDOW_TITLE
        if not isdir(settings.USER_DIR):
            makedirs(settings.USER_DIR)
        if not isdir(settings.CHARSET_USER_DIR):
            makedirs(settings.CHARSET_USER_DIR)
        shutil.copyfile(settings.DEFERRAL_SRC, settings.DEFERRAL_DST)
        shutil.copyfile(settings.ROGUEYUN_SRC, settings.ROGUEYUN_DST)


        self.scene_manager = SceneManager()
        main_menu = TitleScene(self.scene_manager)
        char_gen = CharGenScene(self.scene_manager)
        game_world = GameWorldScene(self.scene_manager)
        self.scene_manager.add_scene("title", main_menu)
        self.scene_manager.add_scene("chargen", char_gen)
        self.scene_manager.add_scene("game_world", game_world)
        self.scene_manager.set_scene("title")

    def handle_input(self):
        key = tcod.console_check_for_keypress(tcod.KEY_PRESSED)

        if key.vk == tcod.KEY_ENTER and key.lalt or key.vk == tcod.KEY_ENTER and key.ralt:
            if tcod.console_is_fullscreen():
                if isfile(self.config_file):
                    config = shelve.open(settings.PERSISTENT_STORAGE, writeback=True)
                    config["settings"]["fullscreen"] = False
                    config.close()
                self.fullscreen = False
                tcod.console_init_root(self.screen_width, self.screen_height, self.window_title, self.fullscreen)
                tcod.mouse_show_cursor(self.use_mouse)
            else:
                if isfile(self.config_file):
                    config = shelve.open(settings.PERSISTENT_STORAGE, writeback=True)
                    config["settings"]["fullscreen"] = True
                    config.close()
                self.fullscreen = True
                tcod.console_init_root(self.screen_width, self.screen_height, self.window_title, self.fullscreen)
                tcod.mouse_show_cursor(self.use_mouse)
            return False

        #elif key.vk == tcod.KEY_ESCAPE:
            #return True

        if self.scene_manager.current_scene != "":
            return self.scene_manager.scenes[self.scene_manager.current_scene].handle_input(key)
        return False
    
    def loop(self):
        #tcod.sys_set_fps(self.limit_fps)
        tcod.console_set_custom_font(self.font_path, self.font_flags)
        tcod.console_init_root(self.screen_width, self.screen_height, self.window_title, self.fullscreen)
        tcod.mouse_show_cursor(self.use_mouse)
        current_time = time.time()
        last_frame_time = 0

        while not tcod.console_is_window_closed():
            current_time = time.time()
            dt = current_time - last_frame_time
            dt = dt - int(dt)
            last_frame_time = current_time

            exit = self.handle_input()
            if exit:
                break
            self.scene_manager.scenes[self.scene_manager.current_scene].update(dt)
            self.scene_manager.scenes[self.scene_manager.current_scene].draw()
            sleep_time = time.time()
            sleep_dt = sleep_time - last_frame_time
            sleep_dt = sleep_dt - int(sleep_dt)
            sleep_frame = settings.TARGET_FPS - sleep_dt
            if sleep_frame > 0:
                time.sleep(sleep_frame)

