# External, non built-in modules
import glfw                         # lean window system wrapper for OpenGL

from core import Node, load, Shader
from transform import translate, identity, rotate, scale
from scene.bird.bird import Bird
from scene.particle import ParticleSystem


class Camp(Node):
	""" Very simple cube based on provided load function """
	def __init__(self, shader, light):
		super().__init__()

		centerX = 0
		centerY = 0
		centerZ = 0
		
		self.transform = translate(centerX, centerY, centerZ)

		firepit = Node(transform=scale(1.2))
		firepit.add(*load(file='scene/firepit/firepit.obj', tex_file='scene/firepit/firepit.png', shader=shader, light_dir=light))

		self.emmiter = ParticleSystem(centerX, centerY, centerZ)

		tentShader = Shader("scene/shaders/texture.vert", "scene/shaders/tent.frag")
		tent = Node(transform=translate(z=11) @ scale(0.5) @ rotate(axis=(0,1,0), angle=-23))
		tent.add(*load(
			file='scene/tent/tent.obj', 
			tex_file='scene/tent/tent.png', 
			normal_file='scene/tent/tent_normal.png',
			shader=tentShader, 
			light_dir=light
			))

		birdShader = Shader("scene/shaders/bird.vert", "scene/shaders/bird.frag")
		self.birdHeight = 20
		self.bird = Node(transform=translate(y=self.birdHeight))
		self.bird.add(Bird(birdShader, light))

		self.add(self.bird)
		self.add(firepit)
		self.add(tent)

	def draw(self, model=identity(), **other_uniforms):
		self.emmiter.draw(**other_uniforms)
		super().draw(model, **other_uniforms)

	def key_handler(self, key):
		if key == glfw.KEY_B:
			if(self.birdHeight > 8):
				self.birdHeight -= 0.05
				self.bird.transform = translate(y=self.birdHeight)

		elif key == glfw.KEY_SPACE:
			if(self.birdHeight < 30):
				self.birdHeight += 0.05
				self.bird.transform = translate(y=self.birdHeight)
