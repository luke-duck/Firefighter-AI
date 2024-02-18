import pygame

class Text(pygame.sprite.Sprite):
    def __init__(self, x, y, text, size, color = "black"):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.text = text
        self.font = pygame.font.SysFont("bahnschrift", size)
        self.surf = self.font.render(self.text, True, color)