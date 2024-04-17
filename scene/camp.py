import sys                          # for system arguments
import random
import math

# External, non built-in modules
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import numpy as np                  # all matrix manipulations & OpenGL args
from itertools import cycle
import glfw                         # lean window system wrapper for OpenGL

from core import Node, load, Mesh
from transform import translate, identity, rotate, scale

class Camp(Node):
    """ Very simple cube based on provided load function """
    def __init__(self, shader):
        super().__init__()
        particle = SmokeParticle(shader=shader)
        #self.add(particle)

        firepit = Node(transform=scale(1.2))
        firepit.add(*load(file='scene/firepit.obj', tex_file='scene/firepit.png', shader=shader))

        tent = Node(transform=translate(z=11) @ scale(0.5) @ rotate(axis=(0,1,0), angle=-23))
        tent.add(*load(file='scene/tent.obj', tex_file='scene/tent.png', shader=shader))

        self.add(firepit)
        self.add(tent)


class ParticleEmmiter:
    def __init__(self):
        pass

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

class Particle(object):
	def __init__(self,x,y,vx,vy,color,size,maxAge = 10):	
		self.x = x		#Position
		self.y = y		
		self.vx =vx		#velocity components
		self.vy = vy

		self.age= 0		
		self.max_age= maxAge
		self.size = size	
		
		self.color=color
		self.is_dead = False

	def update(self,dx=0.05,dy=0.05):
		self.vx += dx* self.wind 
		self.vy += dy*self.wind - 9.8/100

		self.vx *= 1- 10/1000
		self.vy *= 1- 10/1000

		self.x += self.vx
		self.y += self.vy
		self.check_particle_age()		

	def draw(self):
		GL.glColor4fv(self.color)
		GL.glPushMatrix()
		GL.glTranslatef(self.x,self.y,0)
		GL.glutSolidSphere(self.size,20,20)
		GL.glPopMatrix()
		GL.glutPostRedisplay()

	def check_particle_age(self):		
		self.age +=1 
		self.is_dead = self.age >= self.max_age	

		#Start ageing
		self.color[3]= 1.0 - float(self.age)/float(self.max_age)
            
class ParticleSystem():
	'''Container class for the Simulation.
	Takes care to add Exploders at a given interval
	'''
	def __init__(self):		
		self.x = 0
		self.y = 0
		self.timer = 0
		self.particleList = []

	def addParticle(self):
		speed = 5
		speed *= (1 - random.uniform(0,5)/100)
		angle = 270*3.14/180 + round(random.uniform(-0.5,0.5),2)
		vx = speed * math.cos(angle) 
		vy = -speed * math.sin(angle)
		
		f = Particle(30,10,vx,vy,(0.8,0.8,0.8,1),12)			
		self.particleList.append(f)

	def update(self):
		# Clock to launch fireworks,
		interval = 30
		self.timer += 1

		if self.timer % interval == 0 or self.timer < 2:		
			self.addParticle()
		
		for i in range(len(self.particleList)-1,0,-1):
			p = self.particleList[i]
			x = 0.01
			y = 0				
			p.update(x,y)
			p.check_particle_age()			
			if p.is_dead:					
				p.color = [0.0,0.0,0.0,0.0]				
				self.particleList.pop(i)				
			else:
				p.draw()