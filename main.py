from core import Viewer, Shader
from terrain.terrain import Terrain

def main():
    viewer = Viewer()
    #load skybox
    #TODO

    #load files necessary for terrain generation
    terrainShader = Shader("terrain/terrain.vert", "terrain/terrain.frag")
    viewer.add(Terrain(terrainShader))
    viewer.run()

if __name__ == "__main__":
    main()
