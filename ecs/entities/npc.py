from ecs.entities.entity import Entity
from ecs.components.mob import Mob
from ecs.components.health import Health
from ecs.components.glyph import Glyph
from ecs.components.light import LightRadius
from ecs.components.stats import Stats
from ecs.components.actor import Actor
from ecs.components.goap import GOAPBrain
from game.util.constants import Palette
from game.util.dice import d6
from game.util.constants import *
class Npc(Entity):
    def __init__(self, world, slots, groups, hd, hdmodifieramt, strength, dexterity,
                 constitution, intelligence, wisdom, charisma):
        super().__init__()
        world.add_component(self.metadata.entity_id, Mob(slots, groups, hd))
        world.add_component(self.metadata.entity_id, Health(hd, d6, hdmodifieramt, [], d6(hd, "+", hdmodifieramt)))
        world.add_component(self.metadata.entity_id, Glyph(CP437_CHAR_SMILIE_INV, Palette.WHITE.value, Palette.BLACK.value))
        world.add_component(self.metadata.entity_id, Stats(strength, dexterity, constitution, intelligence, wisdom, charisma))
        world.add_component(self.metadata.entity_id, Actor(dexterity/2, False))
        world.add_component(self.metadata.entity_id, LightRadius())
        world.add_component(self.metadata.entity_id, GOAPBrain())