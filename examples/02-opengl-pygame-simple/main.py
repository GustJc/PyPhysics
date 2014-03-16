import sys
sys.path.append("../../modules")
from mymath import *


from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame
import draw

position = [0,0,-10]
wired = True
instructions = True
tx_instruction = None
texture = 0
lightpos = [0,1]

def resize_gl_screen(size):
  width = size[0]
  height = size[1]

  OpenGL.GL.glViewport(0,0, width, height)
  OpenGL.GL.glMatrixMode(OpenGL.GL.GL_PROJECTION)
  OpenGL.GL.glLoadIdentity()
  OpenGL.GLU.gluPerspective(45, 1.0*width/height, 0.1, 100.0)
  OpenGL.GL.glMatrixMode(OpenGL.GL.GL_MODELVIEW)
  OpenGL.GL.glLoadIdentity()

def init_gl():
  OpenGL.GL.glShadeModel(GL_SMOOTH)
  OpenGL.GL.glClearColor(0.3, 0.3, 0.3, 0.0)
  OpenGL.GL.glClearDepth(1.0)
  glEnable(GL_DEPTH_TEST)

  #lights
  glEnable(GL_COLOR_MATERIAL)
  glEnable(GL_LIGHTING)
  glEnable(GL_LIGHT0)
  glLight(GL_LIGHT0, GL_POSITION,  (0, 1, 1, 0))

  #Blend
  glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
  #Lighs intensity
  glMaterial(GL_FRONT, GL_AMBIENT, (0.1, 0.1, 0.1, 1.0))
  glMaterial(GL_FRONT, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))

  #glut
  glutInit()

def draw_gl_scene():
  OpenGL.GL.glClear(OpenGL.GL.GL_COLOR_BUFFER_BIT | OpenGL.GL.GL_DEPTH_BUFFER_BIT)
  OpenGL.GL.glLoadIdentity()

  glBegin(GL_QUADS)
  glColor3f(1.0   ,1.0    ,1.0)
  glNormal3f(0    ,0      , 1);
  glVertex3f(10.0  ,-10.0 ,-30)
  glVertex3f(10.0  ,10.0  ,-30)
  glVertex3f(-10.0 ,10.0  ,-30)
  glVertex3f(-10.0 ,-10.0 ,-30)
  glEnd()

  glTranslate(position[0],position[1],position[2])
  glColor3f(0.9   ,0.2  ,0.0)
  if wired:
    glutWireSphere(2,20,20)
  else:
    glutSolidSphere(2,20,20)

  glTranslate(3, 0, 0)
  glColor3f(0.5,0.5,0.5)
  if wired:
    glutWireTeapot(2)
  else:
    glutSolidTeapot(2)

def main():
  """ Main function """
  pygame.init()

  myfont = pygame.font.SysFont("monospace", 16)
  tx_instruction = myfont.render("Arrows to move.CTRL distance.SHIFT light height.H to hide text.", 0, (255,0,0) )


  size = (640, 480)
  #Create a opengl display
  screen = pygame.display.set_mode(size, pygame.OPENGL | pygame.DOUBLEBUF)

  resize_gl_screen(size)
  init_gl()

  #Game
  done = False
  texture = draw.loadImage(tx_instruction)
  drawlist = draw.createTexDL(texture)

  while not done:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        done = True
      if event.type == pygame.KEYDOWN:
        #Move sphere LEFT/RIGHT
        if event.key == pygame.K_LEFT:
          if event.mod & pygame.KMOD_SHIFT:
            global lightpos
            lightpos[0] -= 1
            glLight(GL_LIGHT0, GL_POSITION,  (lightpos[0], lightpos[1], 1, 0))
          else:
            position[0] -= 1
        elif event.key == pygame.K_RIGHT:
          if event.mod & pygame.KMOD_SHIFT:
            lightpos[0] += 1
            glLight(GL_LIGHT0, GL_POSITION,  (lightpos[0], lightpos[1], 1, 0))
          else:
            position[0] += 1
          #UP KEY
        elif event.key == pygame.K_UP:
          if event.mod & pygame.KMOD_CTRL:
            position[2] -= 1
          elif event.mod & pygame.KMOD_SHIFT:
            lightpos[1] += 1
            glLight(GL_LIGHT0, GL_POSITION,  (lightpos[0], lightpos[1], 1, 0))
          else:
            position[1] += 1
            #DOWN KEY
        elif event.key == pygame.K_DOWN:
          if event.mod & pygame.KMOD_CTRL:
            position[2] += 1
          elif event.mod & pygame.KMOD_SHIFT:
            lightpos[1] -= 1
            glLight(GL_LIGHT0, GL_POSITION,  (lightpos[0], lightpos[1], 1, 0))
          else:
            position[1] -= 1

        elif event.key == pygame.K_w:
          global wired
          wired = not wired
        elif event.key == pygame.K_h:
          instructions = not instructions

    draw_gl_scene()

    draw.flat(640, 480)
    glColor3f(1,1,1)
    draw.drawTexture(drawlist, (5, 0) )
    draw.unflat(640, 480)

    pygame.display.flip()

  draw.deleteTexture(texture)
  draw.deleteDL(drawlist)
  pygame.quit()



if __name__ == '__main__':
  main()