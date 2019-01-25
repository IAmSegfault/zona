from ecs.entities.entity import Entity
from ecs.components.volume import Volume
from ecs.components.position import Position3D


class MapTile(Entity):
    def __init__(self, world, x, y, z):
        tags = ["tile"]
        super().__init__(world, "tile", tags, templates=None)
        self.metadata.containers["vicinities"] = []
        self.metadata.containers["static_actors"] = []
        self.metadata.containers["actors"] = []
        world.add_component(self.metadata.entity_id, Volume(False, True))
        world.add_component(self.metadata.entity_id, Position3D(x, y, z))