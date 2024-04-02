from core import Viewer, Shader
from terrain.terrain import Terrain

def main():
    viewer = Viewer()
    terrainShader = Shader("terrain/terrain.vert", "terrain/terrain.frag")
    viewer.add(Terrain(terrainShader))
    viewer.run()

if __name__ == "__main__":
    main()
