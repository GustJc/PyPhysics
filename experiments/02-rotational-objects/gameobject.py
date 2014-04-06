import sys
sys.path.append("../../modules")
import pygame
from physics.body2d import body2d

from myglobals import *

class gameobject(pygame.sprite.Sprite):
  def __init__(self, px, py, image_sprite, groups=[]):
    #Call parent class Sprite
    self.groups = groups
    pygame.sprite.Sprite.__init__(self, self.groups)

    self.image = image_sprite
    self.image_natural = image_sprite
    self.rect = self.image.get_rect()
    self.body = body2d(px,py)
    self.hitbox = pygame.Rect(0,0,self.rect.w, self.rect.h)

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

  def update_animation_angle(self):
    self.image = pygame.transform.rotate(self.image_natural, self.body.rotation_angle)
    
    #TODO: needs to resize to fit larger images and adjust position accordinly
    dx = self.image.get_rect().w/2 - self.image_natural.get_rect().w/2
    dy = self.image.get_rect().h/2 - self.image_natural.get_rect().h/2
    
    myimage = self.image
    self.image = pygame.Surface(self.image_natural.get_rect().size, flags=pygame.SRCALPHA)


    self.image.blit(myimage, (0, 0), self.image.get_rect().move(dx,dy))
    
    

  def update_rotation(self, seconds):
    #TODO: Calculate Inercia torque
    #REMOVE later
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
      self.body.angular_speed = 50
    else:
      self.body.angular_speed = 0

    self.body.angular_speed += self.body.angular_aceleration * seconds
    self.body.rotation_angle += self.body.angular_speed * seconds

    self.update_animation_angle()

  def update(self, seconds):
    self.update_rotation(seconds)
    #async event
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
      self.body.force.y = -1000
    else:
      self.body.force.y = 0

    global gravity_force
    #f = m.a
    #a = m/f
    self.body.aceleration.y = gravity_force
    self.body.aceleration = self.body.aceleration + (self.body.force)/self.body.mass

    self.body.speed += self.body.aceleration*seconds

    if self.body.speed.y > 0 and self.get_hitbox().y >= pygame.display.get_surface().get_height() - self.get_hitbox().h:
      self.body.aceleration.y = self.body.speed.y = 0
    elif self.body.speed.y < 0 and self.get_hitbox().y <= 0:
      self.body.aceleration.y = self.body.speed.y = 0

    self.body.position += self.body.speed*seconds

    self.rect.x = int(self.body.position.x)
    self.rect.y = int(self.body.position.y)
    pass

  #Don't actually gets called with Groups, needs to call manually instead if you want it
  def draw(self, screen):
    screen.blit(self.image, (self.rect.x, self.rect.y) )
    pass

  def events(self, event):
    pass


