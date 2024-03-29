from core import Mesh
from random import randint
import numpy as np
from time import time

class Terrain(Mesh):
    def __init__(self, position, shader):
        self.__init_perlin_noise(int(time()))

        index = list()
        pos = np.array([np.array((i, j, self.__get_noise(i, j, 30, 1/10))) for i in range(100) for j in range(100)])
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
    
    def __init_perlin_noise(self, seed):
        np.random.seed(seed)

        self.perlin = np.array([[np.array(np.random.rand()) for i in range(100)] for j in range(100)])

    def __get_noise(self, x, y, amplitude, freq):
        x *= freq
        coord_x = int(x) % 200
        if (coord_x >= 100):
            coord_x = 199 - coord_x

        y *= freq
        coord_y = int(y) % 200
        if (coord_y > 100):
            coord_y = 199 - coord_y

        return amplitude * self.__interpolation(x - int(x), y - int(y), self.perlin[coord_x][coord_y], self.perlin[coord_x][coord_y + 1], self.perlin[coord_x + 1][coord_y], self.perlin[coord_x + 1][coord_y + 1])


    def __interpolation(self, x, y, t, u, v, w):
        return (w + t - u - v) * x * y + (v - t) * x + (u - t) * y + t

