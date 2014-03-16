from OpenGL.GL import *
from OpenGL.GLU import *
from pygame import image

def drawTexture(drawlist, pos = (0,0) ):
  # set up texturing
  glEnable(GL_TEXTURE_2D)
  glEnable(GL_BLEND)
  glDisable(GL_LIGHTING)

  #draw
  glPushMatrix()
  glTranslate(pos[0], pos[1], 0)

  glCallList(drawlist)

  glPopMatrix()
  # unset texturing
  glEnable(GL_LIGHTING)
  glDisable(GL_TEXTURE_2D)
  glDisable(GL_BLEND)

#From http://www.pygame.org/wiki/SimpleOpenGL2dClasses?parent=CookBook
def loadImage(textureSurface):

  textureData = image.tostring(textureSurface, "RGBA")

  width = textureSurface.get_width()
  height = textureSurface.get_height()

  texture = glGenTextures(1)
  glBindTexture(GL_TEXTURE_2D, texture)
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
  glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA,
      GL_UNSIGNED_BYTE, textureData)

  return texture, width, height

def deleteTexture(texture):
  glDeleteTextures(texture)

def flat(width, height):

  glLoadIdentity()
  glMatrixMode(GL_PROJECTION)
  glLoadIdentity();
  # this puts us in quadrant 1, rather than quadrant 4
  gluOrtho2D(0, width, height, 0)
  glMatrixMode(GL_MODELVIEW)

def unflat(width, height):
  glViewport(0,0, width, height)
  glMatrixMode(OpenGL.GL.GL_PROJECTION)
  glLoadIdentity()
  gluPerspective(45, 1.0*width/height, 0.1, 100.0)
  glMatrixMode(OpenGL.GL.GL_MODELVIEW)
  glLoadIdentity()

#From http://www.pygame.org/wiki/SimpleOpenGL2dClasses?parent=CookBook
def createTexDL(tex_image):
  texture = tex_image[0]
  width = tex_image[1]
  height = tex_image[2]
  newList = glGenLists(1)
  glNewList(newList,GL_COMPILE);
  glBindTexture(GL_TEXTURE_2D, texture)
  glBegin(GL_QUADS)

  # Bottom Left Of The Texture and Quad
  glTexCoord2f(0, 0); glVertex2f(0, 0)

  # Top Left Of The Texture and Quad
  glTexCoord2f(0, 1); glVertex2f(0, height)

  # Top Right Of The Texture and Quad
  glTexCoord2f(1, 1); glVertex2f( width,  height)

  # Bottom Right Of The Texture and Quad
  glTexCoord2f(1, 0); glVertex2f(width, 0)
  glEnd()
  glEndList()

  return newList

def deleteDL(list):
  glDeleteLists(list, 1)


#TODO create class to draw 2d image, load pygame images to opengl texture, etc