import tcod

class Rng(object):
    def __init__(self, seeds, offsets=None):
        self.generator = None
        if offsets is not None and len(seeds) >= len(offsets):
            self.generator = [tcod.random_new_from_seed(seeds[i] + offsets[i], algo=tcod.RNG_MT) for i in range(seeds)]
        else:
            self.generator = [tcod.random_new_from_seed(i, algo=tcod.RNG_MT) for i in seeds]
        self.seed = seeds
        self.offset = offsets
        self.count = [0 for i in self.generator]
