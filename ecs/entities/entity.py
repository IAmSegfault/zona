import esper
from uuid import uuid4
from ecs.components.metadata import MetaData

class Entity(object):
    def __init__(self, world, name=None, tags=None, templates=None):
        if tags is None:
            tags = ["entity"]
        self.metadata = MetaData(world, name, tags, templates)
