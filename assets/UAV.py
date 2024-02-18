import pygame
import os
import random

mainDir = os.path.join(os.path.dirname(__file__), '..')
spriteDir = os.path.join(mainDir, 'sprites')

class UAV(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites/drone/Drone.png").convert_alpha()
        
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.update(x,y,50, 50)
        

        #self.surf = pygame.Surface()
        

    def moveRight(self):
        self.x += 50
        self.rect.update(self.x,self.y,50,50)

    def moveLeft(self):
        self.x -= 50
        self.rect.update(self.x,self.y,50,50)

    def moveUp(self):
        self.y -= 50
        self.rect.update(self.x,self.y,50,50)

    def moveDown(self):
        self.y += 50
        self.rect.update(self.x,self.y,50,50)
