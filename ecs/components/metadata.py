from uuid import uuid4

class MetaData(object):
    def __init__(self, world, name, tags=None, templates=None):
        self.entity_id = world.create_entity()
        #The id to use when saving the entity to save.h5
        self.global_id = str(uuid4())
        #A friendly name
        self.name = name
        #A list of types the entity is
        self.tags = tags
        #Static entities that the entity inherits components from
        self.templates = templates
        #Other entities that are contained in this entity
        self.containers = {}
        self.is_hot = True
        world.add_component(self.entity_id, self)