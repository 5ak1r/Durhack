import pygame
import numpy as np
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 800
CELL_SIZE = 3
GRID_WIDTH, GRID_HEIGHT = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE

# Colors
WHITE = (0, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Set up the display
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life")

#Function to draw the grid
def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        for y in range(0, HEIGHT, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(window, WHITE, rect, 1)


def draw_cells(grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[y][x] == 1:
                pygame.draw.rect(window, WHITE, rect)
            else:
                pygame.draw.rect(window, BLACK, rect)
# Function to color a cell in the grid
def color_cell(pos, color):
    x, y = pos
    grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
    if grid[grid_y][grid_x] == WHITE:
        
        grid[grid_y][grid_x] = color
        rect = pygame.Rect(grid_x * CELL_SIZE, grid_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(window, color, rect)
        pygame.display.flip()
        return True
    else:
        return False

# Main game loop
running = True
click_count = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and click_count < 20:
            mouse_pos = event.pos
            color = BLUE if click_count < 10 else RED
            if color_cell(mouse_pos, color):
                click_count += 1

                
def update_grid(grid):
    new_grid = grid.copy()
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            # Count the number of live neighbors
            num_neighbors = np.sum(grid[y-1:y+2, x-1:x+2]) - grid[y, x]
            # Apply Conway's rules

            #killing a cell: grid[y,x] == 1 means there was a living cell
            if grid[y, x] == 1 and (num_neighbors < 2 or num_neighbors > 3): 
                new_grid[y, x] = 0

            #give birth to a new cell, grid[y,x] == 0 means there was a no cell originally
            elif grid[y, x] == 0 and num_neighbors == 3:
                new_grid[y, x] = 1
    return new_grid

# Initialize grid
grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
# Optional: Set up some initial live cells for testing
for _ in range((GRID_WIDTH * GRID_HEIGHT) // 10):  # Randomly fill ~10% of the grid
    grid[np.random.randint(0, GRID_HEIGHT)][np.random.randint(0, GRID_WIDTH)] = 1

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update game state
    grid = update_grid(grid)
    
    # Render the game
    window.fill(BLACK)  # Fill the screen with black
    draw_cells(grid)
    # draw_grid()  # Optional: draw the grid
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    pygame.time.Clock().tick(10)  # Slower tick for visualization purposes

# Clean up Pygame
pygame.quit()
sys.exit()
