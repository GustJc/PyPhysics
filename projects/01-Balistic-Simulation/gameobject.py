import sys
sys.path.append("../../modules")
import pygame
from physics.body2d import body2d
from math import sqrt

from myglobals import *

class gameobject(pygame.sprite.Sprite):
  def __init__(self, px, py, image_sprite, groups=[]):
    #Call parent class Sprite
    self.groups = groups
    pygame.sprite.Sprite.__init__(self, self.groups)

    self.image = image_sprite
    self.rect = self.image.get_rect()
    self.body = body2d(px,py)
    self.hitbox = pygame.Rect(0,0,self.rect.w, self.rect.h)
    self.active = False

    # Resistencia ar
    self.K = 0.5 * 1.2 * 0.02 * 0.1

  def get_hitbox(self):
    return pygame.Rect(self.rect.x + self.hitbox.x, self.rect.y + self.hitbox.y, 
                        self.hitbox.w, self.hitbox.h)

  def set_hitbox(self, x, y, w, h):
    self.hitbox.x = x
    self.hitbox.y = y
    self.hitbox.w = self.rect.w + w
    self.hitbox.h = self.rect.h + h

  def load_image(self, filename):
    self.image = pygame.image.load(filename).convert()
    self.rect = self.image.get_rect()

  def update(self, seconds):

    #async event
    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_SPACE]:
    #   self.active = True
      

    if not self.active:
      self.rect.x = int(self.body.position.x)
      self.rect.y = int(self.body.position.y)
      return
    
    global gravity_force
    #f = m.a
    #a = f/m
    self.body.force.y = self.body.force.x = 0
    self.body.force.y += gravity_force*self.body.mass
    self.body.force.y += -self.K*sqrt(self.body.speed.x**2 + self.body.speed.x**2)*self.body.speed.y
    self.body.force.y += -self.K*sqrt(self.body.speed.x**2 + self.body.speed.x**2)*self.body.speed.y
    
    self.body.aceleration = (self.body.force)/self.body.mass

    self.body.speed += self.body.aceleration*seconds

    if self.body.speed.y > 0 and self.get_hitbox().y >= pygame.display.get_surface().get_height() - self.get_hitbox().h:
      self.body.aceleration.y = 0
      self.body.speed.y = -self.body.speed.y*self.body.bouncy
      if self.body.speed.y >= -1:
        self.body.speed.y = 0
    elif self.body.speed.y < 0 and self.get_hitbox().y <= 0:
      self.body.aceleration.y = self.body.speed.y =  0

    self.body.position += self.body.speed*seconds

    self.rect.x = int(self.body.position.x)
    self.rect.y = int(self.body.position.y)
    if self.body.position.x > pygame.display.get_surface().get_width():
      self.active = False;
    pass

  #Don't actually gets called with Groups, needs to call manually instead if you want it
  def draw(self, screen):
    screen.blit(self.image, (self.rect.x, self.rect.y) )
    pass

  def events(self, event):
    pass


