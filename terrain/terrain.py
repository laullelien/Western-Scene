from core import Mesh
import numpy as np
import OpenGL.GL as GL
from random import randint
from time import time


class Terrain(Mesh):
    def __init__(self, shader):
        self.size = 100
        self.mountain_number = 4
        self.mountain_radius = 6
        # TODO make sure mountains do not intersect
        self.mountain_points = [np.array([randint(0, self.size - 1), randint(0, self.size - 1)])]
        while len(self.mountain_points) != self.mountain_number:
            peek = True
            new_point = np.array([randint(0, self.size - 1), randint(0, self.size - 1)])
            for point in self.mountain_points:
                if np.linalg.norm(new_point - point) < 4 * self.mountain_radius:
                    peek = False
                    break
            if peek:
                self.mountain_points.append(new_point)

        self.__init_perlin_noise(int(time()))

        self.matL = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [-3, 3, -2, -1], [2, -2, 1, 1]])
        self.matR = np.array([[1, 0, -3, 2], [0, 0, 3, -2], [0, 1, -2, 1], [0, 0, -1, 1]])

        index = list()
        pos = np.array([np.array((i, j, self.__get_height(i, j, 2, 1 / 10))) for i in range(self.size) for j in range(self.size)])
        norm = np.zeros(shape = (self.size * self.size, 3))

        for i in range(self.size - 1):
            for j in range (self.size - 1):
                i1 = self.size * i + j
                i2 = self.size * i + j + 1
                i3 = self.size * (i + 1) + j
                i4 = self.size * (i + 1) + j + 1

                index.append(i1)
                index.append(i3)
                index.append(i2)
                n1 = np.cross(pos[i2] - pos[i1], pos[i3] - pos[i1])
                norm[i1] += n1
                norm[i2] += n1
                norm[i3] += n1

                index.append(i3)
                index.append(i4)
                index.append(i2)
                n2 = np.cross(pos[i2] - pos[i1], pos[i3] - pos[i1])
                norm[i2] += n2
                norm[i3] += n2
                norm[i4] += n2


        for i in range (self.size ** 2):
            norm[i] /= np.linalg.norm(norm[i])
        
        super().__init__(shader, attributes = dict(normal = norm,position = pos), index = index)
    
    def __init_perlin_noise(self, seed):
        np.random.seed(seed)

        self.perlin = np.array([[np.array(np.random.rand()) for i in range(self.size)] for j in range(self.size)])

    def __get_height(self, x, y, amplitude, freq):
        x *= freq
        x_coords = [(int(x) + i) % (2 * self.size) for i in range(-2,4)]
        for i in range(6):
            if x_coords[i] >= self.size:
                x_coords[i] = (2 * self.size - 1) - x_coords[i]

        y *= freq
        y_coords = [(int(y) + i) % (2 * self.size) for i in range(-2,4)]
        for i in range(6):
            if y_coords[i] >= self.size:
                y_coords[i] = (2 * self.size - 1) - y_coords[i]

        f = [[amplitude * self.perlin[x_coords[i]][y_coords[j]]  for j in range(6)] for i in range(6)]

        return self.__bicubic_interpolation(x - int(x), y - int(y), f) + self.__mountain_map(x / freq, y / freq, 15)


    # f is a 6x6 array containing images of f
    def __bicubic_interpolation(self, x, y, f):
        fx = [[(f[i + 1][j] - f[i - 1][j]) / 2 for j in range (1, 5)] for i in range(1, 5)]

        fy = [[(f[i][j + 1] - f[i][j - 1]) / 2 for j in range (1, 5)] for i in range(1, 5)]

        fxy = [[(fy[i + 1][j] - fy[i - 1][j] + fx[i][j + 1] - fx[i][j - 1]) / 4 for j in range(1, 3)] for i in range(1, 3)]
        # See https://en.wikipedia.org/wiki/Bicubic_interpolation

        matF = np.array([[f[2][2], f[2][3], fy[1][1], fy[1][2]], [f[3][2], f[3][3], fy[2][1], fy[2][2]], [fx[1][1], fx[1][2], fxy[0][0], fx[0][1]], [fx[2][1], fx[2][2], fxy[1][0], fxy[1][1]]])

        interpolation = np.array([1, x, x ** 2, x ** 3]) @ self.matL @ matF @ self.matR @ np.array([[1], [y], [y ** 2], [y ** 3]])

        return interpolation.item()

    def __mountain_map(self, x, y, height):
        for mountain_top in self.mountain_points:
            dist = np.sqrt((x - mountain_top[0]) ** 2 + (y - mountain_top[1]) ** 2)
            if (dist <= self.mountain_radius):
                return height + 1 * np.random.rand()
            elif dist <= 2 * self.mountain_radius:
                return 1 * (height + np.random.rand()) / 2 * (2 * self.mountain_radius - dist) / (self.mountain_radius)
        return 0

    def draw(self, primitives=GL.GL_TRIANGLES, attributes=None, **uniforms):
        super().draw(primitives, attributes = attributes, **uniforms)