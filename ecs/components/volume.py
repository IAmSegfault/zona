class Volume(object):
    def __init__(self, solid, transparent=False, block_sight=None):
        self.solid = solid
        self.transparent = transparent
        if block_sight is None:
            if solid and not transparent:
                block_sight = solid
            elif solid and transparent:
                block_sight = not transparent
            elif transparent and not solid:
                block_sight = not transparent
            else:
                block_sight = True
        self.block_sight = block_sight