import sys
sys.path.append("../../modules")
from mymath import *


from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import pygame

position = [0,0,0]
posinc = 10 #Increase pos with each key
wired = True
instructions = True
texture = 0
lightpos = [0,0]
show_fps = True
rotateAngle = 0.0
renderCalls = [GL_TRIANGLES, GL_LINE_STRIP, GL_LINES, GL_LINE_LOOP, GL_POINTS, GL_TRIANGLE_STRIP, GL_TRIANGLE_FAN, GL_QUADS, GL_QUAD_STRIP, GL_POLYGON]
call_id = 0
anim_id = 0
rotating = True
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

def getNames(filename, numbers):
  names = []

  for i in range(numbers):
    names.append(filename+'_')
    if i < 100000:
      n = i+1
      while n < 100000:
        n*=10
        names[i] += '0'

      names[i]+= str(i+1) + ".obj"
  return names

def loadAnimation(filename, frames=1):
  """Load animations, use name without .obj
    Returns a list o DL
  """
  print "Loading..."
  drawlists = []
  names = getNames(filename, frames)
  for idx, name in enumerate(names):
    verts, norms = loadOBJ(name)
    drawlists.append( createDL(verts, norms) )
    print "{0} loaded of {1}".format(idx+1, frames)
  return drawlists
  print "...Loaded"

def unloadAnimation(drawlists):
  for idx, dl_id in enumerate(drawlists):
    glDeleteLists(dl_id, 1)
    print "{0} unloaded".format(idx+1)

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



verts, norms = loadOBJ("data_triangulated/jump_000001.obj")
verts2, norms2 = loadOBJ("data/jump_000001.obj")

drawing_list = 0
drawing_list2 = 0
anim_list = 0

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

def draw_gl_scene(nextframe = False):
  OpenGL.GL.glClear(OpenGL.GL.GL_COLOR_BUFFER_BIT | OpenGL.GL.GL_DEPTH_BUFFER_BIT)
  OpenGL.GL.glLoadIdentity()

  glColor3f(0.5,0.5,1)

    #Draw triangulated mesh at left side of screen
  glPushMatrix()
  glTranslate(-25,0,-80)
  glTranslate(position[0],position[1],position[2])
  global rotateAngle
  global rotating
  glRotatef(rotateAngle,0,1,0)
  #Draw triangulated
  glCallList(drawing_list)
  glPopMatrix()

  #Draw messy mesh at right side of screen
  glPushMatrix()
  glTranslate(25,0,-80)
  glTranslate(position[0],position[1],position[2])
  glRotatef(rotateAngle,0,1,0)
  #Draw triangulated
  glCallList(drawing_list2)
  glPopMatrix()


  #Change animation
  global anim_id
  if nextframe:
    anim_id+=1
    if anim_id >= len(anim_list):
      anim_id = 0

    #Draw animation
  glPushMatrix()
  glTranslate(0,0,-80)
  glTranslate(position[0],position[1],position[2])
  glRotatef(rotateAngle,0,1,0)
  glCallList(anim_list[anim_id])
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
  global drawing_list2
  global anim_list
  drawing_list = createDL(verts, norms)
  drawing_list2 = createDL(verts2, norms2)

  anim_list = loadAnimation("data_triangulated/jump", 55)

  #Game
  done = False
  last_ticks = pygame.time.get_ticks()
  time = 0
  time_frame = 0
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
            global posinc
            position[0] -= posinc
        elif event.key == pygame.K_RIGHT:
          if event.mod & pygame.KMOD_SHIFT:
            lightpos[0] += 1
            glLight(GL_LIGHT0, GL_POSITION,  (lightpos[0], lightpos[1], 1, 0))
          else:
            position[0] += posinc
          #UP KEY
        elif event.key == pygame.K_UP:
          if event.mod & pygame.KMOD_CTRL:
            position[2] -= posinc
          elif event.mod & pygame.KMOD_SHIFT:
            lightpos[1] += 1
            glLight(GL_LIGHT0, GL_POSITION,  (lightpos[0], lightpos[1], 1, 0))
          else:
            position[1] += posinc
            #DOWN KEY
        elif event.key == pygame.K_DOWN:
          if event.mod & pygame.KMOD_CTRL:
            position[2] += posinc
          elif event.mod & pygame.KMOD_SHIFT:
            lightpos[1] -= 1
            glLight(GL_LIGHT0, GL_POSITION,  (lightpos[0], lightpos[1], 1, 0))
          else:
            position[1] -= posinc

        elif event.key == pygame.K_f:
          global show_fps
          show_fps = not show_fps
        #change drawing mode
        elif event.key == pygame.K_a:
          global call_id
          call_id-=1
          if call_id < 0:
            call_id = len(renderCalls)-1
          createDL(verts, norms, drawing_list)
          createDL(verts2, norms2, drawing_list2)
          printRenderName(call_id)
        elif event.key == pygame.K_d:
          call_id+=1
          if call_id > len(renderCalls)-1:
            call_id = 0
          createDL(verts, norms, drawing_list)
          createDL(verts2, norms2, drawing_list2)
          printRenderName(call_id)
          #reset to triangle
        elif event.key == pygame.K_s:
          call_id=0
          createDL(verts, norms, drawing_list)
          createDL(verts2, norms2, drawing_list2)
          printRenderName(call_id)
        #stop rotation
        elif event.key == pygame.K_r:
          global rotating
          rotating = not rotating
        elif event.key == pygame.K_e:
          angle = 90

    #update rotation
    if rotating:
      angle += elapsed_time*0.1
      if angle >= 360:
        angle -= 360

    global rotateAngle
    rotateAngle = math.cos(math.radians(angle))*45

    nextframe = False
    # 24 fps (41 ms ) -> change animation frame
    if time_frame >= 41:
      time_frame -= 41
      nextframe = True
    draw_gl_scene(nextframe)

    pygame.display.flip()
    elapsed_time = pygame.time.get_ticks() - last_ticks
    time += elapsed_time
    time_frame += elapsed_time
    last_ticks = pygame.time.get_ticks()
    fps += 1
    if time > 1000:
      time -= 1000

      poly = len(verts)
      poly2 = len(verts2)
      if show_fps:
        # animation should stays with a consistent poly count
        print("Aproximate polygons: ", poly2+poly*2 )
        print("FPS: ", fps)
      fps = 0

  glDeleteLists(drawing_list, 1)
  glDeleteLists(drawing_list2, 1)
  unloadAnimation(anim_list)
  pygame.quit()



if __name__ == '__main__':
  main()