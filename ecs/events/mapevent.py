import events

class MapEvents(events.Events):
    __events__ = ('move_chunk', 'move_superchunk', 'move_map')

