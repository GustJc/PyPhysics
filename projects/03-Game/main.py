import pygame
import src.sprite as game

pygame.init()
screen = pygame.display.set_mode((400,300))
done = False

GameUpdateList = []
GameRenderList = []

catapult = game.Sprite("data/img/catapult.png", 5)

boulder = None

catapultAnim = game.Animation(catapult, 96, 96, 5, 100)

GameUpdateList.append(catapultAnim)
GameRenderList.append(catapultAnim)
# Testes --------------------------------------
def shotBoulder(dt):
  global boulder
  if( catapultAnim.isReady() ):
    catapultAnim.pause = True
    catapultAnim.forceFrame()
    if(boulder == None):
      boulder = game.Sprite("data/img/boulder.png")
      boulder.pos[0] = 46
      boulder.pos[1] = 7
      GameRenderList.append(boulder)
      
  if(boulder != None):
    dt *= 0.001
    boulder.pos[0] += 300*dt
    boulder.pos[1] += 15*dt

    if(boulder.pos[0] > screen.get_width()):
      GameRenderList.remove(boulder)
      boulder = None
      catapultAnim.forceFrame(0)
      catapultAnim.pause = False
# Testes --------------------------------------

last_time = pygame.time.get_ticks()
while not done:
  screen.fill((255,255,255))
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      done = True

  # Atualiza tempo
  dt = pygame.time.get_ticks() - last_time
  last_time = pygame.time.get_ticks()

  # Atualiza timer da catapulta em ms
  for obj in GameUpdateList:
    obj.update(dt)
    #catapultAnim.update(dt)  

  shotBoulder(dt)
  
  for obj in GameRenderList:
    obj.render(screen)
    #catapultAnim.render(screen)

  # Mostra tela
  pygame.display.flip()

pygame.quit()

