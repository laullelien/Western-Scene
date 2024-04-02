import OpenGL.GL as GL 

#https://learnopengl.com/Advanced-OpenGL/Cubemaps
# https://www.youtube.com/watch?v=ZwNDBOUmyLY  17:40

def loadSkybox(list_image): 
    texture = GL.glGenTextures(1)
    GL.glBindTexture(GL_TEXTURE_CUBE_MAP, texture)

    for i in range(len(list_image)):
        #bla
   
