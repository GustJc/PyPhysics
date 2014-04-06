import pygame

class lineMaker():
  def __init__(self):
    self.pontos = []

  def add(self, ponto):
    self.pontos.append(ponto)

  def draw(self, display):
    for i in range(len(self.pontos)-1):
      pygame.gfxdraw.line(display, self.pontos[i][0], self.pontos[i][1], self.pontos[i+1][0], self.pontos[i+1][1], (0,255,0) )