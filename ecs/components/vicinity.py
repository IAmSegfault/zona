from ecs.enum.vicinity import VicinityType, VicinityID, VicinityColor
from game.util.constants import Palette
class Vicinity(object):
    def __init__(self, transparent=True, walkable=True, vicinity_type="dirt"):
        self.transparent = transparent
        self.walkable = walkable
        self.vtype = VicinityID(".", "#000000", "floor", True, True)
        self.supertype = self.vtype.supertype
        self.color_fg = Palette.WHITE.value
        self.color_bg = Palette.BLACK.value
        for t in VicinityType:
            if t.name == vicinity_type:
                self.vtype = t.value
                break

        for t in VicinityColor:
            if t.name == vicinity_type:
                self.color_fg = t.value[0].value
                self.color_bg = t.value[1].value
                break
