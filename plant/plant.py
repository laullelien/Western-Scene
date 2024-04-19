import sys                          # for system arguments

# External, non built-in modules
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import numpy as np                  # all matrix manipulations & OpenGL args
from itertools import cycle
import glfw                         # lean window system wrapper for OpenGL

from core import Shader, Mesh, Viewer, Node, load
from transform import translate, identity, rotate, scale

class Cube(Node):
    """ Very simple cube based on provided load function """
    def __init__(self, shader):
        super().__init__()
        self.add(*load(file='plant/cube.obj', tex_file='plant/cube.png', shader=shader))  # just load cube from file

class Cactus(Node):
    def __init__(self, shader, pos):
        super().__init__()

        cube = Cube(shader)

        trunk = Node(transform=translate(pos[0], pos[1], pos[2]) @ scale(x=1,y=5,z=1) @ rotate(axis=(0,1,0), angle=-45))
        trunk.add(cube)

        branch1 = Node(transform=translate(z=1.3, y=0.15) @ scale(x=0.5,y=0.13,z=1.8) @ rotate(angle=90))
        branch1.add(cube)

        branch11 = Node(transform=translate(z=-1.5, y=0.35) @ rotate(angle=-90) @ scale(x=1,y=2,z=0.3))
        branch11.add(cube)

        branch1.add(branch11)

        branch2 = Node(transform=translate(z=-1.3, y=-0.10) @ scale(x=0.5,y=0.1,z=1.8) @ rotate(angle=-90))
        branch2.add(cube)

        branch21 = Node(transform=translate(z=1.5, y=0.35) @ rotate(angle=90) @ scale(x=1,y=2,z=0.3))
        branch21.add(cube)

        branch2.add(branch21)

        trunk.add(branch1)
        trunk.add(branch2)

        self.add(trunk)  # just load cube

def addCactus(viewer, terrain, shader, numCactus):
    for i in range(numCactus):
        pos = terrain.get_free_location(10)
        #TODO: add cactus.height/2 to pos[1]
        viewer.add(Cactus(shader, pos))
