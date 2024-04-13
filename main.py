from core import Viewer, Shader
from terrain.terrain import Terrain
from plant.plant import Cactus

def main():
    viewer = Viewer()
    #load skybox
    #TODO

    #load files necessary for terrain generation
    terrainShader = Shader("terrain/terrain.vert", "terrain/terrain.frag")
    #viewer.add(Terrain(terrainShader))

    #load plants
    treeShader = Shader("plant/plant.vert", "plant/plant.frag")
    viewer.add(Cactus(treeShader))
    viewer.run()

if __name__ == "__main__":
    main()
