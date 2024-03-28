from core import Mesh
from random import randint
import numpy as np

class Terrain(Mesh):
    def __init__(self, position, shader):
        index = list()
        pos = np.array([np.array((i, j, randint(0, 10))) for i in range(100) for j in range(100)])
        norm = np.zeros(shape = (10000, 3))

        for i in range(99):
            for j in range (99):
                i1 = 100 * i + j
                i2 = 100 * i + j + 1
                i3 = 100 * (i + 1) + j
                i4 = 100 * (i + 1) + j + 1

                index.append(i1)
                index.append(i2)
                index.append(i3)
                n1 = np.cross(pos[i2] - pos[i1], pos[i3] - pos[i1])
                norm[i1] += n1
                norm[i2] += n1
                norm[i3] += n1

                index.append(i3)
                index.append(i2)
                index.append(i4)
                n2 = np.cross(pos[i2] - pos[i1], pos[i3] - pos[i1])
                norm[i2] += n2
                norm[i3] += n2
                norm[i4] += n2


        for i in range (10000):
            norm[i] /= np.linalg.norm(norm[i])
        
        super().__init__(shader, attributes = dict(normal = norm,position = pos), index = index)