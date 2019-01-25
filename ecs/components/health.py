import tcod

class Health(object):
    def __init__(self, hit_dice, hitdice_type, modifier, hitdice_progression, maxhp):
        self.hit_dice = hit_dice
        self.hitdice_type = hitdice_type
        self.modifier = modifier
        self.hitdice_progression = hitdice_progression
        self.maxhp = maxhp
        self.hp = maxhp