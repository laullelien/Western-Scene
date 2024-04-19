
import math

from core import Node, load
from transform import vec, quaternion_from_euler
from animation import KeyFrameControlNode

class Bird(Node):
    def __init__(self, shader, light):
        super().__init__()

        animationResolution = 20
        radius = 10

        translate_keys = self.points_on_circle(radius, animationResolution) #{0: vec(0,0,0)} 
        rotate_keys = self.rotation_in_place(animationResolution) #{0: quaternion()} 
        scale_keys = {0: 0.1}
        keynode = KeyFrameControlNode(translate_keys, rotate_keys, scale_keys)

        keynode.add(*load(file='scene/bird/bird.obj', shader=shader, light_dir=light))  # just load cube from file
        self.add(keynode)

    def points_on_circle(self, radius, num_points):
        points = {}
        for i in range(num_points):
            angle = i * (2 * math.pi / num_points)
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)
            points[i] = vec(x, 0, z)

        points[num_points] = points[0]
        return points
    
    def rotation_in_place(self, num_points):
        rotation_keys = {}
        for i in range(num_points):
            angle = -360 * (i / num_points)
            rotation_keys[i] = quaternion_from_euler(0, angle, 0)
            
        rotation_keys[num_points] = rotation_keys[0]
        return rotation_keys