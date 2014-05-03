import sys
sys.path.append("../")
import pygame

class Sprite():
  def __init__(self, filename = None, frameX = None, frameY = None):
    if(filename != None):
      self.surf = pygame.image.load(filename)
      self.rect = [0, 0, self.surf.get_width(), self.surf.get_height()]
    else:
      self.surf = None
      self.rect = None

    # Corta baseado em divisoes iguais baseadas nos frames
    if(frameX != None):
      self.rect[2] = self.rect[2] / frameX
    if(frameY != None):
      self.rect[3] = self.rect[3] / frameY

    self.pos = [0.0, 0.0]

  def loadImage(self, filename):
    self.surf = pygame.image.load(filename)

  def render(self, screen):
    screen.blit(self.surf, self.pos, self.rect )

  def setCrop(self, rect):
    self.rect = rect

class Animation():
  '''Somente horizontal'''
  def __init__(self, sprite, frameSizeX, frameSizeY, frames = 1, time = 0 ):
    self.image = sprite
    self.frame_sizeX = frameSizeX
    self.frame_sizeY = frameSizeY
    self.max_frames = frames
    self.current_frame = 0
    self.current_time = 0
    self.change_time = time
    self.is_ready = False
    self.pause = False

  def isReady(self):
    return self.is_ready

  def render(self, screen):
    self.image.render(screen)

  def update(self, dt):
    '''Atualiza frame, dt em ms'''
    if(self.pause == True):
      return

    self.is_ready = False
    self.current_time += dt
    # Passou o tempo, atualiza frame
    if(self.current_time >= self.change_time):
      self.current_time -= self.change_time
      self.current_frame+=1
      if(self.current_frame >= self.max_frames):
        self.is_ready = True
        self.current_frame -= self.max_frames
      self.image.setCrop( [self.frame_sizeX*self.current_frame, 0, self.frame_sizeX, self.frame_sizeY] )

  def forceFrame(self, force_frame = -1):
    if(force_frame == -1):
      self.current_frame = self.max_frames-1
    else:  
      self.current_frame = force_frame

    self.image.setCrop( [self.frame_sizeX*self.current_frame, 0, self.frame_sizeX, self.frame_sizeY] )
    self.time = 0
