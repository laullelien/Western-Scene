from core import Viewer, Shader, Mesh
from terrain.terrain import Terrain
from plant.plant import addCactus
from scene.camp import Camp
from scene.bird.bird import Bird
from river.river import River
import OpenGL.GL as GL
from texture import Textured, Texture
from skybox.skybox import Skybox

def main():
    viewer = Viewer()

    #load skybox
    list_image_path = ["skybox/right.bmp", "skybox/left.bmp", "skybox/top.bmp", "skybox/bottom.bmp", "skybox/front.bmp", "skybox/back.bmp"]
   
    skyboxShader = Shader("skybox/skybox.vert", "skybox/skybox.frag")
    skybox = Skybox(skyboxShader, list_image_path);
    
    viewer.add(skybox)

    world_size = 200

    #load files necessary for terrain generation
    terrainShader = Shader("terrain/terrain.vert", "terrain/terrain.frag")
    terrain = Terrain(terrainShader, world_size)
    viewer.add(Textured(terrain, texture = Texture("terrain/texture/rock_texture.jpg")))

    riverShader = Shader("river/river.vert", "river/river.frag")
    viewer.add(River(riverShader, world_size))

    #load plants
    textureShader = Shader("scene/shaders/texture.vert", "scene/shaders/texture.frag")
    addCactus(viewer, terrain, textureShader, 10)

    colorShader = Shader("plant/color.vert", "plant/color.frag")

    viewer.add(Camp(textureShader, (1, -0.5, 0)))

    #viewer.add(Bird(Shader("scene/shaders/bird.vert", "scene/shaders/bird.frag")))

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
