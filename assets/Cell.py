import pygame
import enum

class FireStatus(enum.Enum):
    BURNED = 0
    BURNING = 1
    NOT_BURNED = 2

class Cell(pygame.sprite.Sprite):

    def __init__(self, x, y, width_height):
        pygame.sprite.Sprite.__init__(self)
        self.current_state = FireStatus.NOT_BURNED
        self.pos = (x, y)
        # self.size = (width_height, width_height)

        self.green = (115, 230, 0)
        self.red = (230, 0, 0)
        self.black = (0, 0, 0)

        self.color = self.green

        self.image = pygame.Surface(width_height)
        self.image.fill(self.green)
        self.rect = self.image.get_rect()
        self.rect.update((x,y), width_height)
        self.burnt = False


    def setState(self, updated_state):
        if self.current_state == FireStatus.BURNED:
            return
        
        if updated_state == FireStatus.BURNED:
            self.color = self.black
        if updated_state == FireStatus.BURNING and self.current_state != FireStatus.BURNED:
            self.color = self.red
        if updated_state == FireStatus.NOT_BURNED:
            self.color = self.green
        
        self.current_state = updated_state
        self.image.fill(self.color)
