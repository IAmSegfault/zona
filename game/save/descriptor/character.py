import settings
from os.path import isfile
import tables
from tables import *

def create_character(character_template):
    h5 = None
    character_table = None
    character = None
    new_file = False
    if isfile(settings.SAVE_FILE):
        h5 = tables.open_file(settings.SAVE_FILE, 'a')
    else:
        h5 = tables.open_file(settings.SAVE_FILE, 'w')
        new_file = True

    if new_file:
        player = h5.create_group("/", "player", "player data")
        character_table = h5.create_table(player, "character", Character, "character loader")
    else:
        character_table = h5.get_node("/player", "character")

    character = character_table.row
    character['class_name'] = character_template.class_name
    character['strength'] = character_template.strength
    character['dexterity'] = character_template.dexterity
    character['strength'] = character_template.constitution
    character['intelligence'] = character_template.intelligence
    character['wisdom'] = character_template.wisdom
    character['charisma'] = character_template.charisma
    character['hit_dice'] = character_template.hit_dice
    character['hit_dice_modifier'] = character_template.hit_dice_modifier

class Character(IsDescription):
    class_name = StringCol(64)
    character_name = StringCol(64)
    strength = UInt8Col()
    dexterity = UInt8Col()
    constitution = UInt8Col()
    intelligence = UInt8Col()
    wisdom = UInt8Col()
    charisma = UInt8Col()
    hit_dice = UInt64Col()
    hit_dice_modifier = UInt64Col()
    max_hit_points = UInt64Col()
    attack_value = UInt8Col()
    saving_throw = UInt8Col()
    level = UInt64Col()
    xp = UInt64Col()
    num_raises = UInt8Col()
    raise1 = UInt8Col()
    raise2 = UInt8Col()
    raise3 = UInt8Col()
    raise4 = UInt8Col()
    raise5 = UInt8Col()
    num_slots = UInt8Col()
    slot1 = UInt64Col()
    slot2 = UInt64Col()
    slot3 = UInt64Col()
    slot4 = UInt64Col()
    slot5 = UInt64Col()
    slot6 = UInt64Col()
    slot7 = UInt64Col()
    slot8 = UInt64Col()
    slot9 = UInt64Col()
    slot10 = UInt64Col()
    num_groups = UInt8Col()
    group1 = UInt64Col()
    group2 = UInt64Col()
    group3 = UInt64Col()
    group4 = UInt64Col()
    group5 = UInt64Col()
