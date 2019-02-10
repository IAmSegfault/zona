import os
import appdirs
APP = 'zona'
DEVELOPER = 'supergamedev'
WINDOW_TITLE = 'Zona'
VERSION = {"major": 0, "minor": 1, "bugfix": 0}
CONSOLE_WIDTH = 80
CONSOLE_HEIGHT = 50
TARGET_FPS = 1.0/24.0
# Folders
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
GAME_DIR = ROOT_DIR + "/game"
DATA_DIR = GAME_DIR + "/data"
USER_DIR = appdirs.user_data_dir(APP, DEVELOPER)
CHARSET_DIR = GAME_DIR + "/character_set"
CHARSET_USER_DIR = USER_DIR + "/character_set"
TEMP_DIR = USER_DIR + "/tmp"
MAP_DIR = DATA_DIR + "/staticmap"
KEYMAP_DIR = USER_DIR + "/keymap"
DEFAULT_KEYMAP_DIR = DATA_DIR + "/keymap"
NEWGAME_DIR = DATA_DIR + "/newgame"
INPUTMAP_DIR = DATA_DIR + "/inputmap"
INPUTMAP_USER_DIR = USER_DIR + "/inputmap"

#Files
PERSISTENT_STORAGE = USER_DIR + "/storage"
SAVE_FILE = USER_DIR + "/save.h5"
LOG_FILE = USER_DIR + "/logfile.log"
GAME_BOOTLOADER = TEMP_DIR + "/bootloader.json"
WORLD_MAP = MAP_DIR + "/world_map.csv"
NEWGAME_POSITION = NEWGAME_DIR + "/position.json"
GAMEWORLD_INPUT = INPUTMAP_DIR + "/gameworld.json"



# Fonts
CP437 = CHARSET_DIR + '/CP437.png'
DEFERRAL_SRC = CHARSET_DIR + "/Deferral-Square-10-cp437.png"
ROGUEYUN_SRC = CHARSET_DIR + "/16x16_sm_ascii.png"

DEFERRAL_DST = CHARSET_USER_DIR + "/Deferral-Square-10-cp437.png"
ROGUEYUN_DST = CHARSET_USER_DIR + "/16x16_sm_ascii.png"

STORAGE_SETTINGS = {"limit_fps": 24, "screen_width": 80, "screen_height": 50, "fullscreen": False,
                    "use_mouse": True, "font": False, "prev_font": CP437}
