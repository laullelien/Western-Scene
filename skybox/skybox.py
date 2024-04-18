import OpenGL.GL as GL 
from PIL import Image
from core import Node, Shader

#https://learnopengl.com/Advanced-OpenGL/Cubemaps
# https://www.youtube.com/watch?v=ZwNDBOUmyLY  17:40


class Skybox():
    def __init__(self, shader, list_image_paths):
        
        self.shader = shader
        self.texture_id = self.load_skybox_texture(list_image_paths)
        
    def load_skybox_texture(self, list_image_paths):
        texture = GL.glGenTextures(1)
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

    def bind(self, unit=0):
        GL.glActiveTexture(GL.GL_TEXTURE0 + unit)
        GL.glBindTexture(GL.GL_TEXTURE_CUBE_MAP, self.texture_id)

    def activate_shader(self):
        self.shader.use()

    def draw(self, primitives=GL.GL_TRIANGLES, attributes=None, **uniforms):
        # Activer le shader de la skybox
        self.activate_shader()

        # Lier la texture de la skybox
        self.bind()

        # Définir les coordonnées des sommets du cube
        skybox_vertices = [
            -1.0,  1.0, -1.0,
            -1.0, -1.0, -1.0,
             1.0, -1.0, -1.0,
             1.0, -1.0, -1.0,
             1.0,  1.0, -1.0,
            -1.0,  1.0, -1.0,

            -1.0, -1.0,  1.0,
            -1.0, -1.0, -1.0,
            -1.0,  1.0, -1.0,
            -1.0,  1.0, -1.0,
            -1.0,  1.0,  1.0,
            -1.0, -1.0,  1.0,

             1.0, -1.0, -1.0,
             1.0, -1.0,  1.0,
             1.0,  1.0,  1.0,
             1.0,  1.0,  1.0,
             1.0,  1.0, -1.0,
             1.0, -1.0, -1.0,

            -1.0, -1.0,  1.0,
            -1.0,  1.0,  1.0,
             1.0,  1.0,  1.0,
             1.0,  1.0,  1.0,
             1.0, -1.0,  1.0,
            -1.0, -1.0,  1.0,

            -1.0,  1.0, -1.0,
             1.0,  1.0, -1.0,
             1.0,  1.0,  1.0,
             1.0,  1.0,  1.0,
            -1.0,  1.0,  1.0,
            -1.0,  1.0, -1.0,

            -1.0, -1.0, -1.0,
            -1.0, -1.0,  1.0,
             1.0, -1.0, -1.0,
             1.0, -1.0, -1.0,
            -1.0, -1.0,  1.0,
             1.0, -1.0,  1.0
        ]

        # Définir le VAO et VBO pour le cube
        cube_vao = GL.glGenVertexArrays(1)
        cube_vbo = GL.glGenBuffers(1)
        GL.glBindVertexArray(cube_vao)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, cube_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, len(skybox_vertices) * 4, (GL.GLfloat * len(skybox_vertices))(*skybox_vertices), GL.GL_STATIC_DRAW)
        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 3 * 4, GL.ctypes.c_void_p(0))

        # Dessiner le cube
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 36)

        # Libérer la mémoire
        GL.glBindVertexArray(0)
        GL.glDeleteBuffers(1, [cube_vbo])
        GL.glDeleteVertexArrays(1, [cube_vao])
    
        