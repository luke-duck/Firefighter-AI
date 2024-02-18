import pygame
from UAV import UAV
from typing import List
from Cell import Cell, FireStatus
import random
from collections import deque

pygame.init()
pygame.key.set_repeat(200, 100)
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
# i = 0
for cel in cell_list:
    # hitboxes[i] = cel.rect
    hitboxes.append(cel.rect)
    # i += 1



uav = UAV(30, 30)
uav_group = pygame.sprite.Group()
uav_group.add(uav)


def check_bounds(start, index):
    if index < 0 or index >= len(cells):
        return False
    
    if start > index and (index) % 9 == 8:
        return False
        
    if start < index and start % 9 == 8:
         return False
    
    return True

# sin0 = 0 cos0 = 1, 
burnt_arr = []

def spread_fire(start_cell: Cell, cellIndex: int, iteration: int):
    if iteration == 0:
        start_cell.setState(FireStatus.BURNING)
        burningQueue.append(cellIndex)
        

    visited = []

    for i in range(len(cells)):
        rng = random.randint(0, 10000)
        # if rng >= chance:
        if rng >= 9950:     # 0.05% chance
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
            

# drone = UAV()
def game_over():
    if len(burnt_arr) > 40: return True
    else: return False

iteration = 0
rand_index = random.randint(0,81)
while running:
    screen.fill("black")
    # game logic
    cell_list.draw(screen)
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_s] and uav.y + 100 < height:
            uav.moveDown()
        elif keys[pygame.K_w] and uav.y - 100 > 0:
            uav.moveUp()
        elif keys[pygame.K_a] and uav.x - 100 > 0:
            uav.moveLeft()
        elif keys[pygame.K_d] and uav.x + 100 < width:
            uav.moveRight()
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
    if won:
        running = False
