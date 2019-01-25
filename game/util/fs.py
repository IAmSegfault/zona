import appdirs
from os import makedirs
from os.path import isfile, isdir

def savefile_exists():
    appname = "zona"
    appauthor = "supergamedev"
    directory = appdirs.user_data_dir(appname, appauthor)
    savefile = directory + "/save.db"

    if isdir(directory):
        if isfile(savefile):
            return True
        else:
            return False
    else:
        makedirs(directory)
        return False

def savefile_path():
    appname = "zona"
    appauthor = "supergamedev"
    directory = appdirs.user_data_dir(appname, appauthor)
    savefile = directory + "/save.db"
    return savefile