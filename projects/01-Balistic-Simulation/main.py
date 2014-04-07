import sys
sys.path.append("../../modules")
from mymath import *
from physics.body2d import body2d
from gameobject import *
from random import randint

import pygame.gfxdraw
import pygame
import math

from line import lineMaker

show_collisions = False
show_text = True
ball_group = pygame.sprite.Group()
active_group = pygame.sprite.Group()
shoot_group = pygame.sprite.Group()
dots_group = pygame.sprite.Group();


class App():
  def __init__(self):
    self._running = True
    self._display_surf = None
    self.size = self.width, self.weight = 640, 480
    self.angle = 65.0
    self.initial_speed = 450.0
    self.ball_sprite = None
    self.counter = 0
    self.dot_delay = 0.1
    self.dot_size  = 5

    self.hide_dot = False
    self.hide_line = False

    self.active = False
    self.rho = 1.2
    self.k = 0.5
    self.Cd = 0.1
    self.A = 0.02
    self.mass = 1.0
    self.K = self.A*self.rho*self.Cd*self.k

    self.color = (255,0,0)

    self.line = [lineMaker()]

  def on_init(self):
    pygame.init()
    self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
    self._running = True
    self.image = pygame.image.load("ball.png")
    self.image = self.image.convert_alpha()
    self.image = pygame.transform.scale(self.image, (45,45) )

    self.ball_sprite = gameobject(10, 440, self.image, active_group)
    self.ball_sprite.rect = self.ball_sprite.image.get_rect()
    self.ball_sprite.set_hitbox(10, 10, -20, -20)
    self.ball_sprite.body.mass = self.mass
    self.ball_sprite.K = self.k * self.rho * self.A * self.Cd

    # red_ball = gameobject(200,92, image.copy() )
    # red_ball.image.fill((80,0,0,127), (red_ball.rect), pygame.BLEND_RGB_ADD)
    # red_ball.set_hitbox(10, 10, -20, -20)
    # red_ball.body.mass = 1.1

    # ball_group.add(red_ball)

    #Font
    self.myfont = pygame.font.SysFont("monospace", 16)
  
    self.tx_instruction = self.myfont.render("Hold space to add force. H to show hitbox. T to hide text.", 0, (255,0,0) )
    self.tx_values = self.myfont.render("Angle: {0} Force: {1} Lines: {2} Dots: {3} Rho: A: {4} Cd: {5} k: {6} K:{7}".format(
                        self.angle, self.initial_speed, self.countLines(), len(dots_group), self.A, self.rho, self.Cd, self.k, self.A*self.rho*self.Cd*self.k ), 0, (255,0,0) ) 

    if self.rho > -0.001 and self.rho < 0.001:
      self.rho = 0
    if self.A > -0.001 and self.A < 0.001:
      self.A = 0
    if self.k > -0.001 and self.k < 0.001:
      self.k = 0
    if self.Cd > -0.001 and self.Cd < 0.001:
      self.Cd = 0
    if self.K > -0.0001 and self.K < 0.0001:
      self.K = 0
    self.tx_values_2 = self.myfont.render("K:{0} = Rho: {1} A: {2} Cd: {3} k: {4}".format(
                         self.K, self.rho, self.A, self.Cd, self.k ), 0, (255,0,0) ) 

  def countLines(self):
    nlines = 0;
    for i in self.line:
      nlines += len(i.pontos)-1
    return nlines

  def on_event(self, event):
    if event.type == pygame.QUIT:
      self._running = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_q:
        global show_collisions
        show_collisions = not show_collisions
      elif event.key == pygame.K_e:
        global show_text
        show_text = not show_text
      elif event.key == pygame.K_a:
        self.angle += 5
      elif event.key == pygame.K_d:
        self.angle -= 5
      
      elif event.key == pygame.K_w:
        self.initial_speed+=10
      elif event.key == pygame.K_s:
        self.initial_speed-=10

      elif event.key == pygame.K_c:
        dots_group.empty()
      elif event.key == pygame.K_x:
        self.line = [self.line[-1] ]

      elif event.key == pygame.K_r:
        self.rho += 0.1
      elif event.key == pygame.K_f:
        self.rho -= 0.1
      elif event.key == pygame.K_t:
        self.A += 0.01
      elif event.key == pygame.K_g:
        self.A -= 0.01
      elif event.key == pygame.K_y:
        self.Cd += 0.1
      elif event.key == pygame.K_h:
        self.Cd -= 0.1
      elif event.key == pygame.K_u:
        self.k += 0.1
      elif event.key == pygame.K_j:
        self.k -= 0.1

      elif event.key == pygame.K_SPACE:
        if not self.active:
          self.ball_sprite.active = True
          self.active = True
          vec = vector2(self.initial_speed * math.cos(math.radians(self.angle)), self.initial_speed * -math.sin(math.radians(self.angle)))
          self.ball_sprite.body.speed += vec
          self.ball_sprite.body.mass = self.mass
          self.ball_sprite.K = self.K
        else:
          self.active = False
          self.changeBalls()
        
  def changeBalls(self):
    ball_group.add(self.ball_sprite)
    self.ball_sprite = gameobject(10, 440, self.image, active_group)
    self.ball_sprite.rect = self.ball_sprite.image.get_rect()
    self.ball_sprite.set_hitbox(10, 10, -20, -20)
    self.ball_sprite.body.mass = self.mass
    self.ball_sprite.K = self.K
    self.line.append(lineMaker())
    self.color = (randint(0,255), randint(0,255), randint(0,255))
    self.line[-1].color = self.color
    pass

  def on_update(self, seconds):
    #async events if needed:
    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_SPACE]:
    self.counter += seconds;
    if(self.counter >= self.dot_delay):
      self.counter -= self.dot_delay
      if self.ball_sprite.active:
        px = (int)(self.ball_sprite.body.position.x + self.ball_sprite.rect.w/2 - self.dot_size/2)
        py = (int)(self.ball_sprite.body.position.y + self.ball_sprite.rect.h/2 - self.dot_size/2)
        # #dot.rect = (5,5,5,5)      
        # #print px, ":", py
        dot = pygame.sprite.Sprite(dots_group)
        dot.image = pygame.Surface((self.dot_size,self.dot_size))
        dot.rect = dot.image.get_rect()
        dot.rect.x = px
        dot.rect.y = py
        dot.image.fill(self.color)
        #linha
        self.line[-1].add( (px, py) )

        #endif
      self.tx_values = self.myfont.render("Angle: {0} Force: {1} Lines: {2} Dots: {3} ".format(
                        self.angle, self.initial_speed, self.countLines(), len(dots_group) ), 0, (255,0,0) ) 
      if self.rho > -0.00001 and self.rho < 0.00001:
        self.rho = 0
      if self.A > -0.00001 and self.A < 0.00001:
        self.A = 0
      if self.k > -0.00001 and self.k < 0.00001:
        self.k = 0
      if self.Cd > -0.00001 and self.Cd < 0.00001:
        self.Cd = 0
      self.K = self.A*self.rho*self.Cd*self.k
      if self.K > -0.0000001 and self.K < 0.0000001:
        self.K = 0
      self.tx_values_2 = self.myfont.render("K:{0} = Rho: {1} A: {2} Cd: {3} k: {4}".format(
                         self.K, self.rho, self.A, self.Cd, self.k ), 0, (255,0,0) ) 
    
    #update
    self.ball_sprite.update(seconds)
    ball_group.update(seconds)
    pass

  def on_render(self):
    self.ball_sprite.draw(self._display_surf)
    ball_group.draw(self._display_surf)
    if not self.hide_dot:
      dots_group.draw(self._display_surf)
    if not self.hide_line:
      for l in self.line:
        l.draw(self._display_surf)

    for ball in ball_group:
      global show_collisions
      if show_collisions:
        pygame.gfxdraw.box(self._display_surf, ball.get_hitbox(), (100,255,0,127))

    if show_collisions:
        pygame.gfxdraw.box(self._display_surf, self.ball_sprite.get_hitbox(), (100,255,0,127))

    global show_text
    if show_text:
      self._display_surf.blit(self.tx_instruction, (5, 5) )
      self._display_surf.blit(self.tx_values, (5,20) )
      self._display_surf.blit(self.tx_values_2, (5,35) )

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
