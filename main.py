from core import Viewer, Shader
from terrain.terrain import Terrain
from river.river import River
from plant.plant import Cactus
from texture import Textured, Texture
from skybox.skybox import Skybox

def main():
    viewer = Viewer()

    #load skybox
    #list_image_path = ["skybox/back.jpg", "skybox/bottom.jpg", "skybox/front.jpg", "skybox/left.jpg", "skybox/right.jpg", "skybox/top.jpg"]
   
    #skyboxShader = Shader("skybox/skybox.vert", "skybox/skybox.frag")
    #skybox = Skybox(skyboxShader, list_image_path);
    
    #viewer.add(skybox)

    world_size = 200

    #load files necessary for terrain generation
    terrainShader = Shader("terrain/terrain.vert", "terrain/terrain.frag")
    viewer.add(Textured(Terrain(terrainShader, world_size), texture = Texture("terrain/texture/rock_texture.jpg")))

    riverShader = Shader("river/river.vert", "river/river.frag")
    viewer.add(River(riverShader, world_size))

    #load plants
    treeShader = Shader("plant/plant.vert", "plant/plant.frag")
    viewer.add(Cactus(treeShader))
    viewer.run()

if __name__ == "__main__":
    main()
