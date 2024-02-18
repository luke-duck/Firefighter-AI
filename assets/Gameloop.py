import pygame
import os
import sys

class Gameloop:

    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        pygame.key.set_repeat(200, 100)
        self.clock = pygame.time.Clock()
        self.state = "Running"

        self.width = 900
        self.height = 500

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Firefighter")

    def loop(self):
        while self.state == "Running":

            


            pygame.display.flip()
            self.clock.tick(60)
