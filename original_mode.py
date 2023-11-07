import pygame
import numpy as np
from constants import * 
import check_criteria


rows, cols = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
grid = np.zeros((rows, cols), dtype=int)  #an array that represents each cell, either 1 or 0 (alive or dead)
# grid_size = (20, 20)
print(grid.shape)



def update_grid_original(grid):
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
def draw_cells(grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[y][x] == 1:
                pygame.draw.rect(screen, WHITE, rect)
            else:
                pygame.draw.rect(screen, BLACK, rect)

def game_over_display(evolution, new_grid):
    font = pygame.font.Font(None, 36)
    # Draw background
    screen.fill((0, 0, 0))

    # Draw text
    text = font.render(f"{evolution}th evolutions, {np.sum(new_grid)} cells left!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(320, 240))
    screen.blit(text, text_rect)

    # Update the display
    pygame.display.flip()

    # Wait for the user to close the window
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

return_button1 = pygame.Rect(30, 30, 20, 20)
def return_button(return_button1):
    pygame.draw.rect(screen, (0, 0, 0), return_button1)

    # Draw return button

    # Draw return button text
    font = pygame.font.Font(None, 14)# Font
    return_text = font.render("Home", True, (255, 255, 255))
    screen.blit(return_text, (return_button1.x, return_button1.y + 1))

    # Update the display
    pygame.display.flip()

def original_game():
    # Initialize Pygame

    pygame.init()

    # Setting up the display
    global screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Initialize the grid with random values
    # param here, can be altered
    grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
    for _ in range((GRID_WIDTH * GRID_HEIGHT) // 10):  # Randomly fill ~10% of the grid
        grid[np.random.randint(0, GRID_HEIGHT)][np.random.randint(0, GRID_WIDTH)] = 1
    ## or just give it random pattern as follows
    # grid = np.random.choice([0, 1], size=(GRID_HEIGHT, GRID_WIDTH))

    # Main game loop
    running = True
    evolution = 0
    while running:
        # Get all events from the event queue
        for event in pygame.event.get():
            # Quit the game if the user closes the screen
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                return_button1 = pygame.Rect(30, 30, 20, 20)
                if return_button1.collidepoint(event.pos):
                    print('trigger!!!')
                    return

        # Update the grid
        new_grid = update_grid_original(grid)
        evolution+=1 # for result counting 
        if check_criteria.check_dead(new_grid) or check_criteria.check_stabilization(grid,new_grid):
            game_over_display(evolution, new_grid)
            running = False

        grid = new_grid
        # Render the game
        screen.fill(BLACK)  # Fill the screen with black
        ###
        draw_cells(grid)

        ## check if the status
        return_button1 = pygame.Rect(30, 30, 20, 20)
        return_button(return_button1)
        # Update the display
        pygame.display.flip()
        # pygame.time.delay(300) # param here, can be altered

    ## what's the result?
    # display the generation lived, count the grid

    # Wait for the user to close the window
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

    # Quit this mode
    return 

