from core import Mesh
from random import randint
import numpy as np

class Terrain(Mesh):
    def __init__(self, position, shader):
        index = list()
        pos = np.array([(i, j, randint(0, 10)) for i in range(100) for j in range(100)])
        for i in range(99):
            for j in range (99):
                index.append(100 * i + j)
                index.append(100 * i + j + 1)
                index.append((100) * (i + 1) + j)
                index.append((100) * (i + 1) + j)
                index.append(100 * i + j + 1)
                index.append((100) * (i + 1) + j + 1)
        
        super().__init__(shader, attributes = dict(position = pos), index = index)