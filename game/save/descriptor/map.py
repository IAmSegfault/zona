from tables import *

class Map3DDescriptor(IsDescription):
    global_id = StringCol(36)
    length = UInt32Col()
    width = UInt32Col()
    height = UInt32Col()
    posX = UInt32Col()
    posY = UInt32Col()
