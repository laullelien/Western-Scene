import sys                          # for system arguments
import random
import math

# External, non built-in modules
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import numpy as np                  # all matrix manipulations & OpenGL args
from itertools import cycle
import glfw                         # lean window system wrapper for OpenGL
import noise

from core import Node, load, Mesh, Shader, Texture
from transform import translate, identity, rotate, scale
from time import time

class Camp(Node):
	""" Very simple cube based on provided load function """
	def __init__(self, shader):
		super().__init__()

		self.emmiter = ParticleSystem()
		self.emmiter.addParticle()

		mesh = Quad(shader)
		#self.add(mesh)

		firepit = Node(transform=scale(1.2))
		firepit.add(*load(file='scene/firepit.obj', tex_file='scene/firepit.png', shader=shader))

		tent = Node(transform=translate(z=11) @ scale(0.5) @ rotate(axis=(0,1,0), angle=-23))
		tent.add(*load(file='scene/tent.obj', tex_file='scene/tent.png', shader=shader))

		self.add(firepit)
		#self.add(tent)

	def draw(self, model=identity(), **other_uniforms):
		self.emmiter.draw(**other_uniforms)
		super().draw(model, **other_uniforms)

class ParticleSystem():
	def __init__(self):		
		self.x = 0
		self.y = 0

		self.t0 = time()
		self.time = 0.0
		self.interval = 0
	
		self.particleList = []

	def addParticle(self):
		vx = 0.05
		vy = 0.05
		vz = 0.05
		
		f = Particle(0,0,0, vx,vy,vz, [0.8,0.8,0.8,1], 0.5)			
		self.particleList.append(f)

	def draw(self, **other_uniforms):		
		if(self.interval > 10):
			self.interval = 0
			if(random.random() < 0.60):
				self.addParticle()

		for i in range(len(self.particleList) - 1,0, -1):
			p = self.particleList[i]		
			p.update(self.time)		
			if p.is_dead:					
				p.color = [0.0,0.0,0.0,0.0]				
				self.particleList.pop(i)				
			else:
				p.draw(**other_uniforms)

		self.interval += glfw.get_time() - self.time
		self.time = time() - self.t0

class Particle():
	def __init__(self, x, y, z, vx, vy, vz, color, size, maxAge = 500):	
		#Position
		self.x = x		
		self.y = y		
		self.z = z
	
		#Speed
		self.vx = vx
		self.vy = vy
		self.vz = vz

		self.age = 0		
		self.max_age = maxAge
		self.size = size	

		self.freqX = random.uniform(0, 1)
		self.freqZ = random.uniform(0, 1)

		self.phaseX = random.uniform(0, 20)
		self.phaseZ = random.uniform(0, 20)

		self.amplitudeX = random.uniform(0, 0.2)
		self.amplitudeZ = random.uniform(0, 0.2)

		self.color = color
		self.is_dead = False

		self.texture = Texture("scene/smoke.png")
		self.quad = Quad(Shader("scene/particle.vert", "scene/particle.frag"))

	def update(self, t):
		currTime = glfw.get_time()
		deltaTime = currTime - t

		noise_x = self.amplitudeX * math.sin(self.freqX * currTime + self.phaseX) * math.sqrt(currTime/10)
		noise_z = self.amplitudeZ * math.sin(self.freqZ * currTime + self.phaseZ) * math.sqrt(currTime/10)


		self.x += self.vx * noise_x * deltaTime
		self.y += self.vy * deltaTime
		self.z += self.vz * noise_z * deltaTime
		self.check_particle_age(deltaTime)

	def draw(self, **other_uniforms):
		other_uniforms["center"] = np.array([self.x, self.y, self.z], dtype=np.float32)
		other_uniforms["size"] = np.array([self.size, self.size], dtype=np.float32)
		other_uniforms["alpha"] = 1 - (self.age / self.max_age)
		#other_uniforms["texture_map"] = self.texture

		self.quad.draw(**other_uniforms)

	def check_particle_age(self, deltaTime):		
		self.age += deltaTime
		self.is_dead = self.age >= self.max_age	


class Quad(Mesh):
	def __init__(self, shader):
		position = np.array(((-0.5, -0.5, 0.0), (0.5, -0.5, 0.0), (0.5,  0.5, 0.0), (-0.5,  0.5, 0.0)), 'f')
		tex_coord = np.array(((0,0), (1,0), (1,1), (0,1)), 'f')
		#color = np.array(((1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)), 'f')
		index = np.array((0, 1, 3, 3, 1, 2), np.uint32)
		self.color = (1, 1, 1)
		attributes = dict(position=position, tex_coord=tex_coord)
		super().__init__(shader, index=index, attributes=attributes)

	def draw(self, primitives=GL.GL_TRIANGLES, **uniforms):
		super().draw(primitives=primitives, global_color=self.color, **uniforms)
