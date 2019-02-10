from ecs.entities.entity import Entity
from ecs.components.vicinity import Vicinity
from ecs.components.position import Position3D
from ecs.components.glyph import FOWGlyph
from game.util.constants import Palette

class MapTile(Entity):
    def __init__(self, world, x, y, z):
        tags = ["maptile"]
        super().__init__(world, "tile", tags, templates=None)
        self.metadata.containers["static_actors"] = []
        self.metadata.containers["actors"] = []
        world.add_component(self.metadata.entity_id, Vicinity())
        vicinity = world.component_for_entity(self.metadata.entity_id, Vicinity)
        world.add_component(self.metadata.entity_id, Position3D(x, y, z))
        world.add_component(self.metadata.entity_id, FOWGlyph(vicinity.vtype.character, vicinity.color_fg,
                                                              vicinity.color_bg))