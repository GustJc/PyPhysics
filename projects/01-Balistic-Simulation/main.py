import sys
sys.path.append("../../modules")
from mymath import *
from physics.body2d import body2d
from gameobject import *

import pygame.gfxdraw
import pygame
import math

from line import lineMaker

show_collisions = False
show_text = True
ball_group = pygame.sprite.Group()
shoot_group = pygame.sprite.Group()
dots_group = pygame.sprite.Group();
tx_instruction = None

class App():
  def __init__(self):
    self._running = True
    self._display_surf = None
    self.size = self.width, self.weight = 640, 480
    self.angle = 45.0
    self.initial_speed = 350.0
    self.ball_sprite = None
    self.counter = 0
    self.dot_delay = 0.1
    self.dot_size  = 5

    self.line = lineMaker()

  def on_init(self):
    pygame.init()
    self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
    self._running = True
    image = pygame.image.load("ball.png")
    image = image.convert_alpha()

    self.ball_sprite = gameobject(50, 92, image, ball_group)
    self.ball_sprite.rect = self.ball_sprite.image.get_rect()
    self.ball_sprite.set_hitbox(10, 10, -20, -20)
    self.ball_sprite.body.mass = 1.0

    red_ball = gameobject(200,92, image.copy() )
    red_ball.image.fill((80,0,0,127), (red_ball.rect), pygame.BLEND_RGB_ADD)
    red_ball.set_hitbox(10, 10, -20, -20)
    red_ball.body.mass = 1.1

    ball_group.add(red_ball)

    #Font
    myfont = pygame.font.SysFont("monospace", 16)
    global tx_instruction
    tx_instruction = myfont.render("Hold space to add force. H to show hitbox. T to hide text.", 0, (255,0,0) )

  def on_event(self, event):
    if event.type == pygame.QUIT:
      self._running = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_h:
        global show_collisions
        show_collisions = not show_collisions
      if event.key == pygame.K_t:
        global show_text
        show_text = not show_text
      if event.key == pygame.K_l:
        vec = vector2(self.initial_speed * math.cos(math.radians(self.angle)), self.initial_speed * -math.sin(math.radians(self.angle)))
        self.ball_sprite.body.speed += vec
      if event.key == pygame.K_w:
        self.angle += 20
      if event.key == pygame.K_s:
        self.angle -= 20
        

  def on_update(self, seconds):
    #async events if needed:
    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_SPACE]:
    self.counter += seconds;
    if(self.counter >= self.dot_delay):
      self.counter -= self.dot_delay
      px = (int)(self.ball_sprite.body.position.x + self.ball_sprite.get_hitbox().w/2 + self.dot_size/2)
      py = (int)(self.ball_sprite.body.position.y + self.ball_sprite.get_hitbox().h/2 + self.dot_size/2)
      # dot = pygame.sprite.Sprite(dots_group)
      # #dot.rect = (5,5,5,5)      
      # print px, ":", py
      # dot.image = pygame.Surface((self.dot_size,self.dot_size))
      # dot.rect = dot.image.get_rect()
      # dot.rect.x = px
      # dot.rect.y = py
      # dot.image.fill((255,0,0))

      #linha
      self.line.add( (px, py) )

    
    
    #update
    ball_group.update(seconds)
    pass

  def on_render(self):
    ball_group.draw(self._display_surf)
    dots_group.draw(self._display_surf)
    self.line.draw(self._display_surf)

    for ball in ball_group:
      global show_collisions
      if show_collisions:
        pygame.gfxdraw.box(self._display_surf, ball.get_hitbox(), (100,255,0,127))

    global show_text
    if show_text:
      self._display_surf.blit(tx_instruction, (5, 5) )

    pygame.gfxdraw.line(self._display_surf, (int)(self.ball_sprite.body.position.x), (int)(self.ball_sprite.body.position.y), 
                        (int)(self.ball_sprite.body.position.x+math.cos(math.radians(self.angle))*50), 
                        (int)(self.ball_sprite.body.position.y+-math.sin(math.radians(self.angle))*50), (255,0,0))
    


  def on_cleanup(self):
    pygame.quit()

  def on_execute(self):
    if self.on_init() == False:
      self._running = False

    last_time = pygame.time.get_ticks()
    while self._running:
      self._display_surf.fill((0,0,0))
      for event in pygame.event.get():
        self.on_event(event)

      dt = pygame.time.get_ticks() - last_time
      dt *= 0.001
      last_time = pygame.time.get_ticks()

      self.on_update(dt)
      self.on_render()
      pygame.display.flip()

    self.on_cleanup()

if __name__ == "__main__":
  theApp = App()
  theApp.on_execute()
