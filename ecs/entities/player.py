from ecs.entities.entity import Entity
from ecs.components.characterclass import CharacterClass
from ecs.components.health import Health
from ecs.components.glyph import Glyph
from ecs.components.dimension import WorldFOWCircle
from game.util.constants import Palette
import logging
import settings

class PlayerCharacter(Entity):
    def __init__(self, world, new_character=True, class_directive=None):
        if new_character and class_directive is not None:

            super().__init__(world, class_directive["name"], ["player", class_directive["classname"]])
            try:
                class_name = class_directive["classname"]
                slots = class_directive["slots"]
                groups = class_directive["groups"]
                attack_value = class_directive["attack_value"]
                saving_throw = class_directive["saving_throw"]
                level = class_directive["level"]
                xp = class_directive["xp"]
                xp_progression = class_directive["xp_progression"]
                attack_value_progression = class_directive["attack_value_progression"]
                saving_throw_progression = class_directive["saving_throw_progression"]
                slot_progression = class_directive["slot_progression"]
                group_progression = class_directive["group_progression"]
                hit_dice = class_directive["hit_dice"]
                hit_dice_type = class_directive["hit_dice_type"]
                hit_dice_modifier = class_directive["hit_dice_modifier"]
                max_hit_points = class_directive["max_hit_points"]
                hit_dice_progression = class_directive["hit_dice_progression"]

                world.add_component(self.metadata.entity_id, CharacterClass(class_name, slots, groups, attack_value,
                                                                            saving_throw, level, xp, xp_progression,
                                                                            slot_progression, group_progression,
                                                                            attack_value_progression,
                                                                            saving_throw_progression))
                world.add_component(self.metadata.entity_id, Health(hit_dice, hit_dice_type, hit_dice_modifier,
                                                                    hit_dice_progression, max_hit_points))

                world.add_component(self.metadata.entity_id, WorldFOWCircle(2))

                world.add_component(self.metadata.entity_id, Glyph("@", Palette.WHITE.value, Palette.BLACK.value))
            except KeyError as e:
                logging.basicConfig(filename=settings.LOG_FILE, format='%(asctime)s - %(name)s - %(levelname)s: %(message)s')
                logging.critical("Could not read directive %s" % e)
                exit(1)