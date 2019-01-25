from tables import *


class IsInitDescriptor(IsDescription):
    global_id = StringCol(36)
    init = UInt8Col()
    trigger = UInt8Col()
    failure = UInt8Col()
    event = StringCol(48)
    arg_count = UInt8Col()


class IsInitArgs(IsDescription):
    global_id = StringCol(36)
    position = UInt8Col()
    argument = StringCol(48)
