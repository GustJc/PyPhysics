#-*- coding: utf8 -*-
import pygame
import numpy as np
from pygame.locals import *
 
pygame.init()
 
class Squares:
    def __init__(self, N, cor=0.5, cor_wall=0.5, max_speed=1000, L=20):
        self.pos = np.empty((N, 2), dtype=float)
        self.pos[:, 0] = np.random.uniform(100, 700, size=N)
        self.pos[:, 1] = np.random.uniform(100, 500, size=N)
     
        self.vel = np.empty((N, 2), dtype=float)
        self.vel[:, 0] = np.random.uniform(-200, 200, size=N)
        self.vel[:, 1] = np.random.uniform(-200, 200, size=N)
 
        self.theta = np.random.uniform(0, 2*np.pi, size=N)
        self.omega = np.random.uniform(-10, 10, size=N)
 
        self.m = np.random.uniform(10, 255, size=N)
        self.cor = cor
        self.cor_wall = cor_wall
        self.max_speed = max_speed
        self.L = L
 
    def update(self, ms):
        dt = ms / 1000.
        #self.vel[:, 1] += 100 * dt
        self.pos += self.vel * dt
        self.theta += self.omega * dt
         
        # Colis천es
        self.collision_wall()
        self.force_max_speed()
         
    def check_rot_col(self, x , y, i, R1, R2 ):
        delta = R2 - R1
        L = np.sqrt(np.dot(delta, delta))
        for s in self.vertices((x, y), self.theta[i]):
            alpha = sum(delta * (s - R1)) / L
            if 0 <= alpha <= L:
                alpha_v = (alpha/L) * delta
                N = np.array([delta[1], -delta[0]])
                if sum(alpha_v * N) >= 0:
                    # Colis찾o!
                    self.vel[i] = (0, 0)
                    self.omega[i] = 0
                    break
    def collision_wall(self):
        r = self.cor_wall
        for i, (x, y) in enumerate(self.pos):
            # Parede da esquerda
            R = self.L * np.sqrt(2) / 2
            if x <= R: 
                R1 = np.array([0, 0])
                R2 = np.array([0, 600])
                self.check_rot_col(x,y,i, R1, R2)
                # self.vel[i] *= (-r, r)
                # self.pos[i, 0] = R
            
            # Parede da direita
            elif x >= 800 - R: 
                R1 = np.array([800, 0])
                R2 = np.array([800, 600])
                self.check_rot_col(x,y,i, R1, R2)
                # self.vel[i] *= (-r, r)
                # self.pos[i, 0] = 800 - R
 
            # Parede de baixo
            if y >= 600 - R: 
                R1 = np.array([0, 600])
                R2 = np.array([800, 600])
                self.check_rot_col(x,y,i, R1, R2)
                 
                #self.vel[i] *= (r, -r)
                #self.pos[i, 1] = 600 - R
 
            # Parede de cima
            elif y <= R: 
                R1 = np.array([0, 600])
                R2 = np.array([800, 600])
                self.check_rot_col(x,y,i, R1, R2)
                # self.vel[i] *= (r, -r)
                # self.pos[i, 1] = R
                 
    def force_max_speed(self):
        vmax = self.max_speed
        for i, (vx, vy) in enumerate(self.vel):
            if vx > vmax: self.vel[i, 0] = vmax
            elif vx < -vmax: self.vel[i, 0] = -vmax
            if vy > vmax: self.vel[i, 1] = vmax
            elif vy < -vmax: self.vel[i, 1] = -vmax
         
    def vertices(self, pos_center, theta):
        r = self.L / 2.0
        A = np.array([-r, r])
        B = np.array([r, r])
        A_ = self.rotate_vector(A, theta)
        B_ = self.rotate_vector(B, theta)
        a = pos_center + A_
        b = pos_center + B_
        c = pos_center - A_
        d = pos_center - B_
        return a, b, c, d
         
    def rotate_vector(self, vector, theta):
        x, y = vector
        cos, sin = np.cos(theta), np.sin(theta)
        x_ = cos * x + sin * y
        y_ = -sin * x + cos * y
        return np.array([x_, y_])
         
    def draw(self, screen):
        for i, (x, y) in enumerate(self.pos):
            m = self.m[i]
            vertices = self.vertices(self.pos[i], self.theta[i])
            pygame.draw.polygon(screen, (m,0,0), vertices, 0)
 
def main():
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    delta_t = 1000./30.
    squares = Squares(30, cor=0.8, cor_wall=0.8, L=40)
 
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()   
                raise SystemExit
                     
        screen.fill((255,255,255))
        squares.update(delta_t)
        squares.draw(screen)
        clock.tick(delta_t)
        pygame.display.flip()
      
if __name__ == '__main__':
    main()