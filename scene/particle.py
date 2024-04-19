import glfw
import OpenGL.GL as GL
import random
import math 
import numpy as np

from core import Shader, Mesh
from time import time

class ParticleSystem():
	def __init__(self, x, y, z):		
		self.x = x
		self.y = y
		self.z = z

		self.t0 = time()
		self.time = 0.0
		self.interval = 0
	
		self.particleList = []

	def addParticle(self):
		vx = 0.8
		vy = 0.5
		vz = 0.8
		
		f = Particle(self.x,self.y + 0.5,self.z, vx,vy,vz, [0.8,0.8,0.8,1], 0.5)			
		self.particleList.append(f)

	def draw(self, **other_uniforms):		
		if(self.interval > 0.5):
			self.interval = 0
			if(random.random() < 0.6):
				self.addParticle()

		for i in range(len(self.particleList) - 1,0, -1):
			p = self.particleList[i]		
			p.update(self.time)		
			if p.is_dead:					
				p.color = [0.0,0.0,0.0,0.0]				
				self.particleList.pop(i)				
			else:
				p.draw(**other_uniforms)

		currTime = glfw.get_time()

		self.interval += currTime - self.time
		self.time = currTime

class Particle():
	def __init__(self, x, y, z, vx, vy, vz, color, size, maxAge = 60):	
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

		self.quad = Quad(Shader("scene/shaders/particle.vert", "scene/shaders/particle.frag"))

	def update(self, t):
		currTime = glfw.get_time()
		deltaTime = currTime - t

		#print(f"Current time: {currTime} Delta time: {deltaTime} Age: {self.age}")

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