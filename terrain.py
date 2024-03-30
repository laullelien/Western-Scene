from core import Mesh
from random import randint
import numpy as np
from time import time

class Terrain(Mesh):
    def __init__(self, position, shader):
        self.__init_perlin_noise(int(time()))

        self.matL = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [-3, 3, -2, -1], [2, -2, 1, 1]])
        self.matR = np.array([[1, 0, -3, 2], [0, 0, 3, -2], [0, 1, -2, 1], [0, 0, -1, 1]])

        index = list()
        pos = np.array([np.array((i, j, self.__get_noise(i, j, 70, 1/20))) for i in range(100) for j in range(100)])
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
        x_coords = [(int(x) + i) % 200 for i in range(-2,4)]
        for i in range(6):
            if x_coords[i] > 100:
                x_coords[i] = 199 - x_coords[i]

        y *= freq
        y_coords = [(int(y) + i) % 200 for i in range(-2,4)]
        for i in range(6):
            if y_coords[i] > 100:
                y_coords[i] = 199 - y_coords[i]

        return amplitude * self.__bicubic_interpolation(x - int(x), y - int(y), x_coords, y_coords)


    def __bicubic_interpolation(self, x, y, x_coords, y_coords):
        f = [[self.perlin[x_coords[i]][y_coords[j]] for j in range(6)] for i in range(6)]

        fx = [[(f[i + 1][j] - f[i - 1][j]) / 2 for j in range (1, 5)] for i in range(1, 5)]

        fy = [[(f[i][j + 1] - f[i][j - 1]) / 2 for j in range (1, 5)] for i in range(1, 5)]

        fxy = [[(fy[i + 1][j] - fy[i - 1][j] + fx[i][j + 1] - fx[i][j - 1]) / 4 for j in range(1, 3)] for i in range(1, 3)]
        # See https://en.wikipedia.org/wiki/Bicubic_interpolation

        matF = np.array([[f[2][2], f[2][3], fy[1][1], fy[1][2]], [f[3][2], f[3][3], fy[2][1], fy[2][2]], [fx[1][1], fx[1][2], fxy[0][0], fx[0][1]], [fx[2][1], fx[2][2], fxy[1][0], fxy[1][1]]])

        interpolation = np.array([1, x, x ** 2, x ** 3]) @ self.matL @ matF @ self.matR @ np.array([[1], [y], [y ** 2], [y ** 3]])

        return interpolation.item()