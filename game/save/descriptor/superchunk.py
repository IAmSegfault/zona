from tables import *

class SuperChunkDescriptor(IsDescription):
    global_id = StringCol(36)
    world_map_posX = UInt32Col()
    world_map_posY = UInt32Col()
    width = UInt32Col()
    height = UInt32Col()
    glyph_character = UInt8Col()
    glyph_foreground_r = UInt8Col()
    glyph_foreground_g = UInt8Col()
    glyph_foreground_b = UInt8Col()
    glyph_background_r = UInt8Col()
    glyph_background_g = UInt8Col()
    glyph_background_b = UInt8Col()
    seed = Int32Col()
    seed_usage_count = UInt64Col()

class LoadedChunksDescriptor(IsDescription):
    # The id of the superchunk
    global_id = StringCol(36)

    # The id of the loaded chunk
    loaded_global_id = StringCol(36)

    loaded_posX = UInt32Col()
    loaded_posY = UInt32Col()

class ChunkSeedsDescriptor(IsDescription):
    global_id = StringCol(36)
    seed = Int32Col()
    posX = UInt32Col()
    posY = UInt32Col()

