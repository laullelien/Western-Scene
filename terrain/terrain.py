import bisect
from core import Mesh
import numpy as np
import OpenGL.GL as GL
from random import randint
from time import time
from terrain.mountain import Mountain

class Terrain(Mesh):
    def __init__(self, shader):
        self.size = 200

        self.__init_mountains(6)
        self.__init_river()
        self.__init_perlin_noise()

        self.matL = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [-3, 3, -2, -1], [2, -2, 1, 1]])
        self.matR = np.array([[1, 0, -3, 2], [0, 0, 3, -2], [0, 1, -2, 1], [0, 0, -1, 1]])

        t0 = time()

        index = np.empty((self.size - 1) * (self.size - 1) * 6, dtype=float)
        norm = np.zeros((self.size * self.size, 3))


        y_indices, x_indices = np.meshgrid(np.arange(self.size), np.arange(self.size))
        z_values = np.vectorize(self.__get_height)(x_indices, y_indices)
        self.pos = np.column_stack((x_indices.flatten(), y_indices.flatten(), z_values.flatten()))


        # Compute indices and normals
        idx = np.arange(0, 6 * (self.size - 1)**2, 6)
        i = np.arange(0, self.size - 1).reshape(-1, 1) * self.size
        j = np.arange(0, self.size - 1)

        i1 = (i + j).flatten()
        i2 = i1 + 1
        i3 = i1 + self.size
        i4 = i2 + self.size

        p1 = self.pos[i1]
        p2 = self.pos[i2]
        p3 = self.pos[i3]
        p4 = self.pos[i4]

        n1 = np.cross(p2 - p1, p3 - p1)
        n2 = np.cross(p3 - p4, p2 - p4)

        norm[i1] += n1
        norm[i2] += n1 + n2
        norm[i3] += n1 + n2
        norm[i4] += n2

        index[idx] = i1
        index[idx + 1] = i3
        index[idx + 2] = i2
        index[idx + 3] = i3
        index[idx + 4] = i4
        index[idx + 5] = i2

        # Normalize normals
        norm /= np.linalg.norm(norm, axis = 1, keepdims=True)

        print("Time taken to generate the terrain:", time() - t0)

        super().__init__(shader, attributes = dict(normal = norm,position = self.pos), index = index)
    
    def __init_mountains(self, mountain_number):
        self.mountains = list()
        self.max_mountain_radius = np.sqrt(self.size * 0.35)
        self.max_mountain_height = np.sqrt(self.size)
        while len(self.mountains) != mountain_number:
            peek = True
            new_point = np.array([randint(int(self.max_mountain_radius * 2), self.size - int(self.max_mountain_radius * 2)), randint(int(self.max_mountain_radius * 2), self.size - int(self.max_mountain_radius * 2))])
            for mnt in self.mountains:
                if np.linalg.norm(new_point - mnt.center) < 4 * self.max_mountain_radius:
                    peek = False
                    break
            if peek:
                rand = np.random.rand()
                self.mountains.append(Mountain(self.max_mountain_height * (0.9 + rand), self.max_mountain_radius * (0.5 * rand + 0.5), new_point))
    
    def __init_perlin_noise(self):
        self.perlin = np.random.rand(self.size, self.size)

    def __get_height(self, x, y):
        amplitude = 1
        freq = .5

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

        #f = [[amplitude * self.perlin[x_coords[i]][y_coords[j]]  for j in range(6)] for i in range(6)]
        mountain_height = self.__mountain_height(x / freq, y / freq)
        river_depth = self.__get_river_depth(x / freq, y / freq)
        f = [[amplitude * self.perlin[x_coords[i]][y_coords[j]] + mountain_height + river_depth for j in range(6)] for i in range(6)]

        #return self.__bicubic_interpolation(x - int(x), y - int(y), f) + self.__mountain_map(x / freq, y / freq)
        return self.__bicubic_interpolation(x - int(x), y - int(y), f)

    # f is a 6x6 array containing images of f
    def __bicubic_interpolation(self, x, y, f):
        fx = [[(f[i + 1][j] - f[i - 1][j]) / 2 for j in range (1, 5)] for i in range(1, 5)]

        fy = [[(f[i][j + 1] - f[i][j - 1]) / 2 for j in range (1, 5)] for i in range(1, 5)]

        fxy = [[(fy[i + 1][j] - fy[i - 1][j] + fx[i][j + 1] - fx[i][j - 1]) / 4 for j in range(1, 3)] for i in range(1, 3)]
        # See https://en.wikipedia.org/wiki/Bicubic_interpolation

        matF = np.array([[f[2][2], f[2][3], fy[1][1], fy[1][2]], [f[3][2], f[3][3], fy[2][1], fy[2][2]], [fx[1][1], fx[1][2], fxy[0][0], fx[0][1]], [fx[2][1], fx[2][2], fxy[1][0], fxy[1][1]]])

        interpolation = np.array([1, x, x ** 2, x ** 3]) @ self.matL @ matF @ self.matR @ np.array([[1], [y], [y ** 2], [y ** 3]])

        return interpolation.item()

    def __mountain_height(self, x, y):
        for mountain in self.mountains:
            dist = np.sqrt((x - mountain.getX()) ** 2 + (y - mountain.getY()) ** 2)
            dist *= (np.random.rand()) / 4 + .9
            if (dist <= mountain.radius):
                return mountain.height + np.random.rand()
            elif dist <= 2 * mountain.radius:
                return 2 * (mountain.height + .5 * np.random.rand()) / 5 * (2 * mountain.radius - dist) / (mountain.radius)
        return 0

    # returns the distance between point a and the line defined by points b and c
    def __dist(self, a, b, c):
        return np.linalg.norm(np.cross(b - c, c - a)) / np.linalg.norm(b - c)

    def __init_river(self):
        self.river_points = list()
        i = 1
        while True:
            intersects_with_mountain = False
            starting_point = np.array([-1, np.random.randint(10, self.size - 10)])
            ending_point = np.array([self.size + 1, np.random.randint(10, self.size - 10)])
            for mountain in self.mountains:
                dist = self.__dist(mountain.center, starting_point, ending_point)
                if (dist <= self.max_mountain_radius * 2):
                    intersects_with_mountain = True
                    break
            if not intersects_with_mountain:
                self.river_points.append(starting_point)
                self.river_points.append(ending_point)
                return
    
    def __in_bound(self, point):
        return point[0] >= 0 and point[1] >= 0 and point[1] < self.size
    
    def __intersect_mountain(self, point):
        for mountain in self.mountains:
            if (np.sqrt((mountain.getX() - point[0]) ** 2 + (mountain.getY() - point[1]) ** 2) < self.max_mountain_radius):
                return True
        return False

    def __get_river_depth(self, x, y):
        river_width = 6 * (1 + np.random.rand() / 3)
        river_depth = 8 * (1 + np.random.rand() / 3)
        dist = self.__dist(np.array([x, y]), self.river_points[0], self.river_points[1])
        if (dist <= river_width):
            dist /= river_width
            return river_depth * (dist ** 2 - 1)
        return 0



