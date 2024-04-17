from core import Viewer, Shader
from terrain.terrain import Terrain
from plant.plant import Cactus
from scene.camp import Camp

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

    viewer.run()

if __name__ == "__main__":
    main()
