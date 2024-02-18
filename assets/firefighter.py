import pygame
import sys
from Cell import Cell, FireStatus
import random
from UAV import UAV
from typing import List
from pygame.constants import K_a, K_d, K_s, K_w
from ple import PLE 
from ple.games.base.pygamewrapper import PyGameWrapper
from deer.agent import NeuralAgent
from deer.learning_algos.q_net_keras import MyQNetwork
import deer.experiment.base_controllers as bc


class Firefighter(PyGameWrapper):

    def __init__(self, width=900, height=900):

        actions = {
            "left": K_a,
            "right": K_d,
            "up": K_w,
            "down": K_s
        }
        PyGameWrapper.__init__(self, width, height, actions=actions)
        self.green = (115, 230, 0)
        self.screen = pygame.display.set_mode((900, 900))

        self.red = (230, 0, 0)
        self.black = (0, 0, 0)
        self.cells_per_row = 9
        self.cells: List[Cell] = []
        self.cell_list = pygame.sprite.Group()
        self.hitboxes = []
        self.uav = UAV(30, 30)
        self.uav_group = pygame.sprite.Group()
        # self.uav_group.add(self.uav)
        self.burnt_arr = []
        self.score = 0
        self.iteration = 0
        self.rand_index = random.randint(0,81)
        self.won = False
        

    def init(self):
        self.score = 0
        self.screen = pygame.display.set_mode((900, 900))
        self.screen.fill("black")

        x_pos = 5
        y_pos = 5

        for j in range(81):
            cell = Cell(x_pos, y_pos, (95, 95))
            self.cell_list.add(cell)
            self.cells.append(cell)
            
            x_pos += 100
            if (j) % 9 == 8:
                y_pos += 100
                x_pos = 5

        self.cell_list.draw(self.screen)
        
        for cel in self.cell_list:
            self.hitboxes.append(cel.rect)

        self.uav = UAV(30, 30)
        self.uav_group.add(self.uav)

    def check_bounds(self, start, index):
        if index < 0 or index >= len(self.cells):
            return False
        
        if start > index and (index) % 9 == 8:
            return False
            
        if start < index and start % 9 == 8:
            return False
        
        return True
    
    def _handle_player_events(self):
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                # running = False
                pygame.quit()
                sys.exit()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_s] and self.uav.y + 100 < self.height:
                self.uav.moveDown()
            elif keys[pygame.K_w] and self.uav.y - 100 > 0:
                self.uav.moveUp()
            elif keys[pygame.K_a] and self.uav.x - 100 > 0:
                self.uav.moveLeft()
            elif keys[pygame.K_d] and self.uav.x + 100 < self.width:
                self.uav.moveRight()
   
    def spread_fire(self, start_cell: Cell, cellIndex: int, iteration: int):
        if iteration == 0:
            start_cell.setState(FireStatus.BURNING)
            

        visited = []

        for i in range(len(self.cells)):
            rng = random.randint(0, 10000)
            # if rng >= chance:
            if rng >= 9950:     # 0.05% chance
                cell = self.cells[i]

                if i + 1 >= len(self.cells):
                    break

                if cell.current_state == FireStatus.BURNING and not cell in visited:
                    if random.randint(0, 10000) >= random.randint(8000, 10000): 
                        cell.setState(FireStatus.BURNED)
                        self.burnt_arr.append(cell)
                        self.score -= 50
                    
                    ran = random.randint(0, 150)

                    if i + self.cells_per_row < len(self.cells):
                        down = self.cells[i+self.cells_per_row]
                        down.setState(FireStatus.BURNING)
                        visited.append(down)
                        self.score -= 50
                        

                    if self.check_bounds(i, i+1):
                        right = self.cells[i + 1]
                        right.setState(FireStatus.BURNING)
                        visited.append(right)
                        self.score -= 50                    
                    if i - self.cells_per_row < len(self.cells) and (i - self.cells_per_row) > 0:
                        up = self.cells[i-self.cells_per_row]
                        up.setState(FireStatus.BURNING)
                        visited.append(up)
                        self.score -= 50

                    if self.check_bounds(i, i-1) and (i -1) > 0:
                        left = self.cells[i - 1]
                        left.setState(FireStatus.BURNING)
                        visited.append(left)
                        self.score -= 50
                
    '''
    100 red —> green
    -50 green —> red
    -100 red —> black
    1,000 all green
    '''
    def getScore(self):
        return self.score
    
    def game_over(self):
        if len(self.burnt_arr) > 40: return True
        else: return False

    def step(self, dt):
        self.screen.fill("black")
        # game logic
        self.cell_list.draw(self.screen)

        self._handle_player_events()

        uav_hitbox = self.uav.rect
        col_index = uav_hitbox.collidelist(self.hitboxes)

        #col_list = pygame.sprite.groupcollide(uav_group, cell_list, False, False)
        if col_index >= 0:
            self.cells[col_index].setState(FireStatus.NOT_BURNED)
            self.score += 100
        
        self.spread_fire(self.cells[self.rand_index], 15, self.iteration)
        self.iteration += 1
        self.uav_group.draw(self.screen)
        self.clock.tick(60)
        if self.iteration > 10:
            self.won = True
            for tile in self.cells:
                if tile.current_state == FireStatus.BURNING:
                    self.won = False
            if self.won:
                self.score += 10000
                


        

if __name__ == "__main__":
    import numpy as np
    pygame.init()
    game = Firefighter(width=900, height =900)
    game.clock = pygame.time.Clock()
    #game.screen = pygame.display.set_mode((width, height))
    game.init()
    

    while True:
        if game.game_over():
            game.init()
        dt = game.clock.tick(60)
        game.step(dt)
        pygame.display.flip()