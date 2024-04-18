from core import Viewer, Shader
from terrain.terrain import Terrain
from plant.plant import Cactus
from scene.camp import Camp
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

    GL.glEnable(GL.GL_BLEND)
    GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
    
    viewer.run()

if __name__ == "__main__":
    main()
