from tables import *


class ChunkDescriptor(IsDescription):
    global_id = StringCol(36)
    width = UInt32Col()
    height = UInt32Col()
    loaded_posX = UInt32Col()
    loaded_posY = UInt32Col()


class LoadedMapsDescriptor(IsDescription):
    global_id = StringCol(36)
    map_global_id = StringCol(36)
    posX = UInt32Col()
    posY = UInt32Col()


class ChunkTags(IsDescription):
    global_id = StringCol(36)
    tag = StringCol(24)