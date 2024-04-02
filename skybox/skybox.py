import OpenGL.GL as GL 

#https://learnopengl.com/Advanced-OpenGL/Cubemaps
# https://www.youtube.com/watch?v=ZwNDBOUmyLY  17:40

def loadSkybox(list_image): 
    texture = GL.glGenTextures(1)
    GL.glBindTexture(GL_TEXTURE_CUBE_MAP, texture)

    for i in range(len(list_image)):
        #bla
        GL.glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, 0, GL.GL_RGB, width, height, 0, GL.GL_RGB, GL.GL_UNSIGNED_BYTE, data)

        #TODO

    GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR);
    GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR);
    GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP_TO_EDGE);
    GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP_TO_EDGE);
    GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_WRAP_R, GL.GL_CLAMP_TO_EDGE);
