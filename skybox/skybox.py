import OpenGL.GL as GL 
from PIL import Image
from core import Node, Shader, Mesh
from texture import Textured
import numpy as np

#https://learnopengl.com/Advanced-OpenGL/Cubemaps
# https://www.youtube.com/watch?v=ZwNDBOUmyLY  17:40


class Skybox(Textured):
    def __init__(self, shader, list_image_paths):
        self.shader = shader
        self.texture_id = self.load_skybox_texture(list_image_paths)
        cube_pos = np.array([[-1.0, -1.0, 1.0], [1.0, -1.0, 1.0], [1.0,  1.0, 1.0], [-1.0, 1.0, 1.0], [-1.0, -1.0, -1.0], [1.0, -1.0, -1.0], [1.0, 1.0, -1.0], [-1.0, 1.0, -1.0]])
        index = np.array([0, 2, 1, 2, 0, 3, 1, 6, 5, 6, 1, 2, 7, 5, 6, 5, 7, 4, 4, 3, 0, 3, 4, 7, 4, 1, 5, 1, 4, 0, 3, 6, 2, 6, 3, 7])
        cube = Mesh(shader, attributes=dict(aPos=cube_pos), index=index)
        super().__init__(cube, textures=self)
        
    def load_skybox_texture(self, list_image_paths):
        self.type = GL.GL_TEXTURE_CUBE_MAP
        self.glid = GL.glGenTextures(1)
        texture = self.glid
        GL.glBindTexture(GL.GL_TEXTURE_CUBE_MAP, texture)

        face_targets = [GL.GL_TEXTURE_CUBE_MAP_POSITIVE_X,
                        GL.GL_TEXTURE_CUBE_MAP_NEGATIVE_X,
                        GL.GL_TEXTURE_CUBE_MAP_POSITIVE_Y,
                        GL.GL_TEXTURE_CUBE_MAP_NEGATIVE_Y,
                        GL.GL_TEXTURE_CUBE_MAP_POSITIVE_Z,
                        GL.GL_TEXTURE_CUBE_MAP_NEGATIVE_Z]

        for i, image_path in enumerate(list_image_paths):
            image = Image.open(image_path)
            image_data = image.convert("RGB").tobytes()
            width, height = image.size
            GL.glTexImage2D(face_targets[i], 0, GL.GL_RGB, width, height, 0, GL.GL_RGB, GL.GL_UNSIGNED_BYTE, image_data)

        GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP_TO_EDGE)
        GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP_TO_EDGE)
        GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_WRAP_R, GL.GL_CLAMP_TO_EDGE)
        
        return texture

    def draw(self, primitives=GL.GL_TRIANGLES, attributes=None, **uniforms):
        GL.glDepthMask(GL.GL_FALSE)
        GL.glDisable(GL.GL_DEPTH_TEST)
        super().draw(primitives, **uniforms)
        GL.glDepthMask(GL.GL_TRUE)