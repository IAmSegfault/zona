from ecs.entities.entity import Entity
from ecs.components.dimension import Rectangle
from ecs.components.position import WorldMapPosition2D
from ecs.components.console import ConsoleHandler


def world_to_camera_pos(viewport, world_x, world_y):
    x = 0
    y = 0
    inbounds = False
    ibreak = False
    for i in range(viewport.x1, viewport.x2):

        for j in range(viewport.y1, viewport.y2):
            if i == world_x and j == world_y:
                inbounds = True
                ibreak = True
                break
            y += 1
        if ibreak:
            break
        x += 1
        y = 0
    if inbounds:
        return x, y
    else:
        return None, None

class AsciiCamera(Entity):
    def __init__(self, world, x1, y1, x2, y2, src_console, xsrc, ysrc, wsrc, hsrc, dst_console, xdst, ydst,
                 fg_alpha=1.0, bg_alpha=1.0, name="asciicamera"):

        super().__init__(world, name, ["camera", "ascii"])
        world.add_component(self.metadata.entity_id, Rectangle(x1, y1, x2, y2))
        world.add_component(self.metadata.entity_id, ConsoleHandler(src_console, xsrc, ysrc, wsrc, hsrc, dst_console,
                                                                    xdst, ydst))