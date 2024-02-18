import pygame
import random
import enum

class FireStatus(enum.Enum):
    BURNED = 0
    BURNING = 1
    NOT_BURNED = 2

class Fire(pygame.sprite.Sprite):
    def __init__(self, scale, img, xpos, ypos):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load(img).convert_alpha()
        self.width = image.get_width()
        self.height = image.get_height()
        self.scale = scale
        
        self.x = xpos
        self.y = ypos
        
        self.originimage = pygame.transform.scale(image, (int(self.width * self.scale), int(self.height) * self.scale))
        self.image = self.originimage
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.status = FireStatus.NOT_BURNED

    def next_burn_stage(self):
        if self.status == FireStatus.NOT_BURNED:
            self.status = FireStatus.BURNING
        elif self.status == FireStatus.BURNING:
            self.status = FireStatus.BURNED

