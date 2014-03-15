import sys
sys.path.append("../../modules")
from mymath import *

import pygame

pygame.init()
screen = pygame.display.set_mode((400,300))

done = False

point_list = []
point_list.append( (10,290) )
point_list.append((390,290))
point_list.append((200,230))
px = 290
last_time = pygame.time.get_ticks()
time = 0
while not done:
  screen.fill((0,0,0))
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      done = True
  # Draw rectangle on screen. (screen, (color), (rect))
  pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(30,30,60,60))
  pygame.draw.circle(screen, (0, 128, 190), (200,200), 20)
  pygame.draw.line(screen, (255, 50,50), (300,200), (350,200), 1)
  pygame.draw.polygon(screen, (255, 100,100), point_list)
  pygame.display.flip()
  
  #update
  elapsed_time = pygame.time.get_ticks() - last_time
  last_time = pygame.time.get_ticks()
  time += elapsed_time
  if(time >= 10):
    time -= 10
    px -= 1
    if(px <= 10):
      px = 390
    point_list[2] = (px, 230)   

pygame.quit()