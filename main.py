from core import Viewer, Shader
from terrain import Terrain

def main():
    viewer = Viewer()
    shader = Shader("color.vert", "color.frag")
    viewer.add(Terrain(1, shader))
    viewer.run()

if __name__ == "__main__":
    main()
