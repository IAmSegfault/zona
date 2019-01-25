class CharacterClass(object):
    def __init__(self, class_name, slots, groups, attack_value, saving_throw, level, xp, xp_progression, slot_progression,
                 group_progression, attack_value_progression, saving_throw_progression):
        self.class_name = class_name
        self.slots = slots
        self.groups = groups
        self.attack_value = attack_value
        self.saving_throw = saving_throw
        self.level = level
        self.xp = xp
        self.xp_progression = xp_progression
        self.slot_progression = slot_progression
        self.group_progression = group_progression
        self.attack_value_progression = attack_value_progression
        self.saving_throw_progression = saving_throw_progression