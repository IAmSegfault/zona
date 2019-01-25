import numpy as np


class ChunkLoader(object):
    def __init__(self, width, height, x, y):
        self.maps = np.zeros((width, height), dtype=np.dtype(object))
        self.loaded_chunk.x = x
        self.loaded_chunk.y = y