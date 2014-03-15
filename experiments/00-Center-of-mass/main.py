import sys
sys.path.append("../../modules")
from mymath import *
from physics.body2d import body2d

import pygame

pygame.init()
screen = pygame.display.set_mode((400,300))

done = False
selectedMass = 0

body_list = []
body_list.append( body2d(100,50) )
body_list.append( body2d(200,50) )
body_list.append( body2d(300,50) )

#Font
myfont = pygame.font.SysFont("monospace", 16)
tx_instruction = myfont.render("Press A and D to select. Click to move", 0, (255,0,0) )
tx_instruction2 = myfont.render("W and S to change mass. Space to add", 0, (255,0,0) )
hide_font = False
while not done:
  screen.fill((0,0,0))

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      done = True
    elif event.type == pygame.MOUSEBUTTONUP and selectedMass >= 0:
      body_list[selectedMass].position.x = pygame.mouse.get_pos()[0]
      body_list[selectedMass].position.y = pygame.mouse.get_pos()[1]
    elif event.type == pygame.MOUSEMOTION and selectedMass >= 0:
      if pygame.mouse.get_pressed()[0]:
        body_list[selectedMass].position.x = pygame.mouse.get_pos()[0]
        body_list[selectedMass].position.y = pygame.mouse.get_pos()[1]
    elif event.type == pygame.KEYDOWN:
      #Mass inputs
      if event.key == pygame.K_w and selectedMass >= 0:
          body_list[selectedMass].mass += 0.25
      elif event.key == pygame.K_s and selectedMass >= 0 and body_list[selectedMass].mass > 0.25:
        body_list[selectedMass].mass -= 0.25
      #Change selectedMass
      elif event.key == pygame.K_a and not len(body_list) == 0:
        if not selectedMass > 0:
          selectedMass = len(body_list)-1
        else:
          selectedMass -= 1
      elif event.key == pygame.K_d and not len(body_list) == 0:
        if not selectedMass < len(body_list)-1:
          selectedMass -= len(body_list)-1
        else:
          selectedMass += 1
      #Text hid
      elif event.key == pygame.K_h:
        hide_font = not hide_font
      #New mass
      elif event.key == pygame.K_SPACE:
        body_list.append(body2d(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
        selectedMass = len(body_list)-1
      #Delete mass
      elif event.key == pygame.K_DELETE and selectedMass >= 0:
        body_list.pop(selectedMass)
        if selectedMass <= len(body_list):
          selectedMass = len(body_list)-1
          print selectedMass

  #Calculate center of mass
  centerMass = vector2(0,0)
  totalMass = 0
  for idx, body in enumerate(body_list):
    color = (0,128,190)
    #Highlight selected mass
    if idx == selectedMass:
      color = (10,88, 100)

    pygame.draw.circle(screen, color, (int(body.position.x), int(body.position.y)), int(20*body.mass))
    centerMass.x += body.position.x*body.mass
    centerMass.y += body.position.y*body.mass
    totalMass += body.mass

  if totalMass != 0:
    centerMass /= totalMass;
  #Center of mass
  pygame.draw.circle(screen, (255, 156, 111), (int(centerMass.x), int(centerMass.y)), 10)
  #Text
  if not hide_font:
    screen.blit(tx_instruction, (5, 5) )
    screen.blit(tx_instruction2, (5, 280) )


  pygame.display.flip()
 	

pygame.quit()

