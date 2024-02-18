import pygame
from typing import List
import random
from collections import deque
from UAV import UAV
from Cell import Cell, FireStatus
from Text import Text

pygame.init()
pygame.font.init()

lose_text = Text(300, 400, "You lose!", 100)
win_text = Text(300, 400, "You win!", 100)

pygame.key.set_repeat(100, 15)
clock = pygame.time.Clock()
running = True
won = False
lost = False

width = 900
height = 900

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Firefighter")

screen.fill("black")

green = (115, 230, 0)
red = (230, 0, 0)
black = (0, 0, 0)

cells_per_row = 9
cells: List[Cell] = []

burningQueue = deque()

x_pos = 5
y_pos = 5

cell_list = pygame.sprite.Group()

for j in range(81):
    cell = Cell(x_pos, y_pos, (95, 95))
    cell_list.add(cell)
    cells.append(cell)
    
    x_pos += 100
    if (j) % 9 == 8:
        y_pos += 100
        x_pos = 5

cell_list.draw(screen)

hitboxes = []
for cel in cell_list:
    hitboxes.append(cel.rect)


uav = UAV(30, 30)
uav_group = pygame.sprite.Group()
uav_group.add(uav)

burnt_arr = []

def check_bounds(start, index):
    if index < 0 or index >= len(cells):
        return False
    
    if start > index and (index) % 9 == 8:
        return False
        
    if start < index and start % 9 == 8:
         return False
    
    return True

def spread_fire(start_cell: Cell, cellIndex: int, iteration: int):
    if iteration == 0:
        start_cell.setState(FireStatus.BURNING)
        burningQueue.append(cellIndex)

    visited = []

    for i in range(len(cells)):
        rng = random.randint(0, 10000)
        if len(burningQueue) < 10:
            chance = 8800
        # elif len(burningQueue) > 40: chance = 9990
        else: chance = 9942
        if rng >= chance:     # 0.05% chance
            cell = cells[i]

            if i + 1 >= len(cells):
                break

            if cell.current_state == FireStatus.BURNING and not cell in visited:
                if random.randint(0, 10000) >= random.randint(8000, 10000): 
                    cell.setState(FireStatus.BURNED)
                    burnt_arr.append(cell)
                
                ran = random.randint(0, 150)

                if i + cells_per_row < len(cells):
                    down = cells[i+cells_per_row]
                    down.setState(FireStatus.BURNING)
                    visited.append(down)
                    burningQueue.append(down)

                if check_bounds(i, i+1):
                    right = cells[i + 1]
                    right.setState(FireStatus.BURNING)
                    visited.append(right)
                    burningQueue.append(right)
                
                if i - cells_per_row < len(cells) and (i - cells_per_row) > 0:
                    up = cells[i-cells_per_row]
                    up.setState(FireStatus.BURNING)
                    visited.append(up)
                    burningQueue.append(up)

                if check_bounds(i, i-1) and (i -1) > 0:
                    left = cells[i - 1]
                    left.setState(FireStatus.BURNING)
                    visited.append(left)
                    burningQueue.append(left)
            

def game_over():
    if len(burnt_arr) > 40: return True
    else: return False

iteration = 0
rand_index = random.randint(16,80)
while running:
    screen.fill("black")
    # game logic
    cell_list.draw(screen)
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
        
        # if keys[pygame.K_s] and keys[pygame.K_d] and uav.y + 30 < height and uav.x + 30 < width:
        #     uav.moveDown()
        #     uav.moveRight()
        # elif keys[pygame.K_d] and keys[pygame.K_w] and uav.x + 30 < width and uav.y - 30 > 0:
        #     uav.moveRight()
        #     uav.moveUp()
        # elif keys[pygame.K_w] and keys[pygame.K_a] and uav.y - 30 > 0 and uav.x - 30 > 0:
        #     uav.moveUp()
        #     uav.moveLeft()
        # elif keys[pygame.K_a] and keys[pygame.K_s] and uav.x - 30 > 0 and uav.y + 30 < height:
        #     uav.moveLeft()
        #     uav.moveDown()

    if keys[pygame.K_s] and uav.y + 30 < height:
        uav.moveDown()
    elif keys[pygame.K_d] and uav.x + 30 < width:
        uav.moveRight()
    elif keys[pygame.K_w] and uav.y - 30 > 0:
        uav.moveUp()
    elif keys[pygame.K_a] and uav.x - 30 > 0:
        uav.moveLeft()
    uav_hitbox = uav.rect
    col_index = uav_hitbox.collidelist(hitboxes)

        #col_list = pygame.sprite.groupcollide(uav_group, cell_list, False, False)
    if col_index >= 0:
        cells[col_index].setState(FireStatus.NOT_BURNED)


    spread_fire(cells[rand_index], 15, iteration)
    
    iteration += 1
    uav_group.draw(screen)


    # refresh screen 60hz
    clock.tick(60)
    pygame.display.flip()
    

    if iteration > 10:
        won = True
        for tile in cells:
            if tile.current_state == FireStatus.BURNING:
                won = False
    if game_over():
        lost = True

    if won:
        # screen.fill("white")
        winscreen = pygame.image.load("../sprites/endgames/forest.jpg")
        winscreen = pygame.transform.scale(winscreen, (900,900))
        screen.blit(winscreen, (0,0))
        screen.blit(win_text.surf, (win_text.x, win_text.y))
        # win_grp.draw(screen)
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False
    if lost:
        # screen.fill("gray")
        losescreen = pygame.image.load("../sprites/endgames/fire.jpg")
        losescreen = pygame.transform.scale(losescreen, (900,900))
        screen.blit(losescreen, (0,0))
        screen.blit(lose_text.surf, (lose_text.x, lose_text.y))
        # lose_grp.draw(screen)
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False
