from core import Viewer, Shader, Mesh
from terrain.terrain import Terrain
from plant.plant import Cactus
from scene.camp import Camp
from scene.bird import Bird
import OpenGL.GL as GL

def main():
    viewer = Viewer()
    #load skybox
    #TODO

    world_size = 200

    #load files necessary for terrain generation
    terrainShader = Shader("terrain/terrain.vert", "terrain/terrain.frag")
    #viewer.add(Terrain(terrainShader, world_size))

    #riverShader = Shader("river/river.vert", "river/river.frag")
    #viewer.add(River(riverShader, world_size))

    #load plants
    textureShader = Shader("scene/texture.vert", "scene/texture.frag")
    #viewer.add(Cactus(textureShader))

    colorShader = Shader("plant/color.vert", "plant/color.frag")

    viewer.add(Camp(textureShader))

    viewer.add(Axis(colorShader))

    GL.glEnable(GL.GL_BLEND)
    GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
    
    viewer.run()

class Axis(Mesh):
    """ Axis object useful for debugging coordinate frames """
    def __init__(self, shader):
        pos = ((0, 0, 0), (1, 0, 0), (0, 0, 0), (0, 1, 0), (0, 0, 0), (0, 0, 1))
        col = ((1, 0, 0), (1, 0, 0), (0, 1, 0), (0, 1, 0), (0, 0, 1), (0, 0, 1))
        super().__init__(shader, attributes=dict(position=pos, color=col))

    def draw(self, primitives=GL.GL_LINES, **uniforms):
        super().draw(primitives=primitives, **uniforms)

if __name__ == "__main__":
    main()
