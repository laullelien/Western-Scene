from core import Viewer, Shader
from terrain.terrain import Terrain
from plant.plant import Tree

def main():
    viewer = Viewer()
    #load skybox
    #TODO

    #load files necessary for terrain generation
    terrainShader = Shader("terrain/terrain.vert", "terrain/terrain.frag")
    viewer.add(Terrain(terrainShader))

    #load plants
    treeShader = Shader("plant/plant.vert", "plant/plant.frag")
    viewer.add(Tree(terrainShader))
    viewer.run()

if __name__ == "__main__":
    main()
