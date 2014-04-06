import sys
sys.path.append("../../modules")
from mymath import *
from physics.body2d import body2d
from gameobject import *

import pygame.gfxdraw
import pygame

show_collisions = False
show_text = True
ball_group = pygame.sprite.Group()
tx_instruction = None

class App():
  def __init__(self):
    self._running = True
    self._display_surf = None
    self.size = self.width, self.weight = 640, 480

  def on_init(self):
    pygame.init()
    self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
    self._running = True
    image = pygame.image.load("ball.png")
    image = image.convert_alpha()

    ball_sprite = gameobject(50, 92, image, ball_group)
    ball_sprite.rect = ball_sprite.image.get_rect()
    ball_sprite.set_hitbox(10, 10, -20, -20)
    ball_sprite.body.mass = 1.0


    red_ball = gameobject(200,92, image.copy() )
    red_ball.image.fill((80,0,0,127), (red_ball.rect), pygame.BLEND_RGB_ADD)
    red_ball.set_hitbox(10, 10, -20, -20)
    red_ball.body.mass = 1.1

    ball_group.add(red_ball)

    bigball_sprite = gameobject(220, -20, pygame.transform.scale(image, (200,200) ), ball_group)
    bigball_sprite.rect = bigball_sprite.image.get_rect()
    bigball_sprite.set_hitbox(25, 25, -50, -50)
    bigball_sprite.body.mass = 1.5

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

  def on_update(self, seconds):
    #async events if needed:
    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_SPACE]:

    #update
    ball_group.update(seconds)
    pass

  def on_render(self):
    ball_group.draw(self._display_surf)

    for ball in ball_group:
      global show_collisions
      if show_collisions:
        pygame.gfxdraw.box(self._display_surf, ball.get_hitbox(), (100,255,0,127))

    global show_text
    if show_text:
      self._display_surf.blit(tx_instruction, (5, 5) )


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
