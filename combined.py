import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Setting up the display
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Conway's Game of Life - Click to Add Cells")

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Cell size and grid
cell_size = 20
rows, cols = height // cell_size, width // cell_size
grid = np.zeros((rows, cols), dtype=int)  #an array that represents each cell, either 1 or 0 (alive or dead)

print(grid.shape)

# Initialize clicks count
clicks = 0

# Draw the grid with blue and red cells
def draw_grid():
    #nested loop, for each row (y), each column element (x)
    for y in range(0, height, cell_size):
        for x in range(0, width, cell_size):
            rect = pygame.Rect(x, y, cell_size, cell_size)
            cell_value = grid[y // cell_size][x // cell_size]

            #case 0: when cell_value = 0, it is a dead cell/empty
            #case 1, when cell_value = 1, it is a red cell
            #case 2: when cell_value = 2, it is a blue cell
            if cell_value == 1:
                pygame.draw.rect(screen, BLUE, rect)
            elif cell_value == 2:
                pygame.draw.rect(screen, RED, rect)
            else:
                pygame.draw.rect(screen, BLACK, rect)

#print(grid)

# Update the grid based on modified rules
def update_grid():
    global grid
    new_grid = grid.copy()
    for y in range(rows):
        for x in range(cols): #loops through each cell. checks for all 8 neighbouring cells and count blues and reds
            neighbors_blue = 0
            neighbors_red = 0
            for j in range(max(0, y-1), min(rows, y+2)):  #iterate through each cell
                for i in range(max(0, x-1), min(cols, x+2)):
                    if j == y and i == x:  #discount the central cell
                        continue
                    if grid[j][i] == 1:
                        neighbors_blue += 1  #increases neighbors_blue counter 
                    elif grid[j][i] == 2:
                        neighbors_red += 1
            total_neighbors = neighbors_blue + neighbors_red

            
            #death case for blue
            if grid[y][x] == 1 and (neighbors_blue < 2 or neighbors_blue > 3):
                new_grid[y][x] = 0

            #death case for red 

            elif grid[y][x] == 2 and (neighbors_red < 2 or neighbors_red > 3):
                new_grid[y][x] = 0

            #birth cases for red/blue. whenever there is a birth, the new cell will take on the colour of the majority neighbout
            elif grid[y][x] == 0 and total_neighbors == 3:
            
                if neighbors_blue > neighbors_red:
                    new_grid[y][x] = 1
                else:
                    new_grid[y][x] = 2
    grid = new_grid

# Main loop
running = True
simulation_started = False
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not simulation_started:
            mouseX, mouseY = pygame.mouse.get_pos()
            gridX, gridY = mouseX // cell_size, mouseY // cell_size
            if grid[gridY][gridX] == 0:  # Check if the cell is not already filled
                clicks += 1
                if clicks <= 10:
                    grid[gridY][gridX] = 1  # Blue cells
                elif clicks <= 20:
                    grid[gridY][gridX] = 2  # Red cells
                if clicks == 21:
                    simulation_started = True

    draw_grid()

    # Start simulation after 20 clicks
    if simulation_started:
        update_grid()

    pygame.display.flip()
    pygame.time.delay(300)  # Delay to slow down the simulation

pygame.quit()
