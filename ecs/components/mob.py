class Mob(object):
    def __init__(self, slots, groups, hd):
        self.slots = slots
        self.groups = groups
        self.attack_value = hd + 10
        self.saving_throw = hd + 5
        if self.saving_throw > 19:
            self.saving_throw = 19
