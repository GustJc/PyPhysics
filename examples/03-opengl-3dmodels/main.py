import sys
sys.path.append("../../modules")
from mymath import *


from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import pygame

position = [0,0,0]
wired = True
instructions = True
useCube = False
texture = 0
lightpos = [0,0]
use_dl = True
show_fps = True
rotateAngle = 0.0

renderCalls = [GL_TRIANGLES, GL_LINE_STRIP, GL_LINES, GL_LINE_LOOP, GL_POINTS, GL_TRIANGLE_STRIP, GL_TRIANGLE_FAN, GL_QUADS, GL_QUAD_STRIP, GL_POLYGON]
call_id = 0
def printRenderName(id):
  if id == 0:
    print "Using GL_TRIANGLES"
  elif id == 1:
    print "Using GL_LINE_STRIP"
  elif id == 2:
    print "Using GL_LINES"
  elif id == 3:
    print "Using GL_LINE_LOOP"
  elif id == 4:
    print "Using GL_POINTS"
  elif id == 5:
    print "Using GL_TRIANGLE_STRIP"
  elif id == 6:
    print "Using GL_TRIANGLE_FAN"
  elif id == 7:
    print "Using GL_QUADS"
  elif id == 8:
    print "Using GL_QUAD_STRIP"
  elif id == 9:
    print "Using GL_POLYGON"
  else:
    print "Not found"


#From http://www.nandnor.net/?p=86, changed to support .obj with no normals without crashing
def loadOBJ(filename):
  numVerts = 0
  verts = []
  norms = []
  vertsOut = []
  normsOut = []
  for line in open(filename, "r"):
    vals = line.split()
    if vals[0] == "v":
      v = map(float, vals[1:4])
      verts.append(v)
    if vals[0] == "vn":
      n = map(float, vals[1:4])
      norms.append(n)
    if vals[0] == "f":
      for f in vals[1:]:
        w = f.split("/")
        # OBJ Files are 1-indexed so we must subtract 1 below
        vertsOut.append(list(verts[int(w[0])-1]))
        if len(f) > 2:
          normsOut.append(list(norms[int(w[2])-1]))
        numVerts += 1
  return vertsOut, normsOut

def drawOBJ(verts, norms):
  glBegin(renderCalls[call_id])

  for normal, vert in enumerate(verts):
    glNormal3fv(norms[normal])
    glVertex3fv(vert)

  glEnd()

def createDL(verts,norms, forcedraw=None):
  drawlist = 0
  if not forcedraw:
    drawlist = glGenLists(1);
  else:
    drawlist = forcedraw

  glNewList(drawlist, GL_COMPILE)

  drawOBJ(verts,norms)

  glEndList()

  return drawlist



verts, norms = loadOBJ("cube.obj")

verts2, norms2 = loadOBJ("gust.obj")

drawing_list = 0
drawing_cube = 0

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
  glLight(GL_LIGHT0, GL_POSITION,  (lightpos[0], lightpos[1], 1, 0))

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

  glColor3f(0.5,0.5,1)
  glPushMatrix()
  glTranslate(0,0,-5)
  glTranslate(position[0],position[1],position[2])
  global rotateAngle
  glRotatef(rotateAngle,0,1,0)

  if use_dl:
    glCallList(drawing_list)
    if useCube:
      glCallList(drawing_cube)
  else:  
    drawOBJ(verts2,norms2)
    if useCube:
      drawOBJ(verts, norms)

  glPopMatrix()

def main():
  """ Main function """
  print "Press H to hide/show cube. Press W to change drawing mode."
  pygame.init()

  size = (640, 480)
  #Create a opengl display
  screen = pygame.display.set_mode(size, pygame.OPENGL | pygame.DOUBLEBUF)

  resize_gl_screen(size)
  init_gl()

  #Create drawlist
  global drawing_list
  drawing_list = createDL(verts2, norms2)
  global drawing_cube
  drawing_cube = createDL(verts, norms)

  #Game
  done = False
  last_ticks = pygame.time.get_ticks()
  time = 0
  fps = 0
  angle = 0
  elapsed_time = 0
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
          global use_dl
          use_dl = not use_dl
        elif event.key == pygame.K_h:
          global useCube
          useCube = not useCube
        #change drawing mode
        elif event.key == pygame.K_a:
          global call_id
          call_id-=1
          if call_id < 0:
            call_id = len(renderCalls)-1
          createDL(verts2, norms2, drawing_list)
          createDL(verts, norms, drawing_cube)
          printRenderName(call_id)
        elif event.key == pygame.K_d:
          call_id+=1
          if call_id > len(renderCalls)-1:
            call_id = 0
          createDL(verts2, norms2, drawing_list)
          createDL(verts, norms, drawing_cube)
          printRenderName(call_id)
          #reset to triangle
        elif event.key == pygame.K_s:
          call_id=0
          createDL(verts2, norms2, drawing_list)
          createDL(verts, norms, drawing_cube)
          printRenderName(call_id)
        elif event.key == pygame.K_f:
          global show_fps
          show_fps = not show_fps

    #update rotation
    angle += elapsed_time*0.1
    if angle >= 360:
      angle -= 360

    global rotateAngle
    rotateAngle = math.cos(math.radians(angle))*45

    #draw scene
    draw_gl_scene()

    pygame.display.flip()
    elapsed_time = pygame.time.get_ticks() - last_ticks
    time += elapsed_time
    last_ticks = pygame.time.get_ticks()
    fps += 1
    if time > 1000:
      time -= 1000

      triangles = len(verts2)
      if useCube:
        triangles += len(verts)
      if show_fps:
        print("Triangles: ", triangles )
        print("FPS: ", fps)
      fps = 0

  glDeleteLists(drawing_list, 1)
  glDeleteLists(drawing_cube, 1)
  pygame.quit()



if __name__ == '__main__':
  main()