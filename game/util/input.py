import json
from os.path import isfile, isdir
import logging
import settings
import tcod
from copy import deepcopy
from os import makedirs

class Mapping(object):
    def __init__(self, keycode, char="", lctrl=False, lalt=False, lmeta=False, rctrl=False, ralt=False,
                 rmeta=False, shift=False):

        self.keycode = keycode
        # Char for non character keycodes should be 0
        self.char = char
        self.lctrl = lctrl
        self.lalt = lalt
        self.lmeta = lmeta
        self.rctrl = rctrl
        self.ralt = ralt
        self.rmeta = rmeta
        self.shift = shift


class InputMap(object):
    def __init__(self, default_static, default, user):
        self.default_static = default_static
        self.default = default
        self.user = user

    def set_keyset(self, filepath):
        if isfile(filepath):
            data = None
            with open(filepath) as f:
                data = json.load(f)

            default_static = data["default_static"]
            default = data["default"]
            user = data["user"]

            static_dict = {}
            default_dict = {}
            user_dict = {}

            try:
                for k, v in default_static.items():
                    keycode = int(v[0])
                    if keycode == tcod.KEY_CHAR:
                        char = str(v[1])
                    else:
                        char = 0
                    lctrl = bool(v[2])
                    lalt = bool(v[3])
                    lmeta = bool(v[4])
                    rctrl = bool(v[5])
                    ralt = bool(v[6])
                    rmeta = bool(v[7])
                    shift = bool(v[8])
                    mst = Mapping(keycode, char, lctrl, lalt, lmeta, rctrl, ralt, rmeta, shift)
                    static_dict[k] = mst

                self.default_static = static_dict

                for k, v in default.items():
                    keycode = int(v[0])
                    if keycode == tcod.KEY_CHAR:
                        char = str(v[1])
                    else:
                        char = 0
                    lctrl = bool(v[2])
                    lalt = bool(v[3])
                    lmeta = bool(v[4])
                    rctrl = bool(v[5])
                    ralt = bool(v[6])
                    rmeta = bool(v[7])
                    shift = bool(v[8])
                    mdef = Mapping(keycode, char, lctrl, lalt, lmeta, rctrl, ralt, rmeta, shift)
                    default_dict[k] = mdef

                self.default = default_dict

                for k, v in user.items():
                    keycode = int(v[0])
                    if keycode == tcod.KEY_CHAR:
                        char = str(v[1])
                    else:
                        char = 0
                    lctrl = bool(v[2])
                    lalt = bool(v[3])
                    lmeta = bool(v[4])
                    rctrl = bool(v[5])
                    ralt = bool(v[6])
                    rmeta = bool(v[7])
                    shift = bool(v[8])
                    musr = Mapping(keycode, char, lctrl, lalt, lmeta, rctrl, ralt, rmeta, shift)
                    user_dict[k] = musr

                self.user = user_dict

            except (KeyError, IndexError) as e:
                logging.basicConfig(filename=settings.LOG_FILE, format='%(asctime)s - %(name)s - %(levelname)s: %(message)s')
                logging.critical("Could not read input map %s" % filepath)
                exit(1)

    def set_mapping(self, action, mapping):
        if action in self.default:
            del self.default[action]
        self.user[action] = mapping

    def unset_mapping(self, action):
        if action in self.default_static and action in self.user:
            del self.user[action]
            self.default[action] = deepcopy(self.default_static[action])

    def save_keyset(self, filepath):
        keyset = {}
        keyset["default_static"] = self.default_static
        keyset["default"] = self.default
        keyset["user"] = self.user
        with open(filepath, 'w') as f:
                json.dump(keyset, f)

