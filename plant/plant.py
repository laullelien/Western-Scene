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
        self.add(*load('plant/cube.obj', shader))  # just load cube from file

class Tree(Node):
    def __init__(self, shader):
        super().__init__()

        cube = Cube(shader)

        trunk = Node(transform=scale(x=1,y=5,z=1))
        trunk.add(cube)

        branch1 = Node(transform=translate(z=1.5, y=0.45) @ scale(x=0.5,y=0.1,z=2) @ rotate(angle=90))
        branch1.add(cube)

        branch1 = Node(transform=translate(z=1.5, y=0.45) @ scale(x=0.5,y=0.1,z=2) @ rotate(angle=90))
        branch1.add(cube)

        branch11 = Node(transform=translate(z=-1.5, y=0.45) @ scale(x=0.5,y=0.1,z=2) @ rotate(angle=-90))
        branch11.add(cube)

        branch1.add(branch11)

        branch2 = Node(transform=translate(z=-1.3, y=0.35) @ scale(x=0.5,y=0.1,z=1.8) @ rotate(angle=-90))
        branch2.add(cube)

        trunk.add(branch1)
        trunk.add(branch2)

        self.add(trunk)  # just load cube