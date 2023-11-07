import pygame
import numpy as np
from constants import * 
import check_criteria

# Setting up the display
width, height = 640, 480


# Cell size and grid
cell_size = 20
rows, cols = height // cell_size, width // cell_size

grid = np.zeros((rows, cols), dtype=int)

# Initialize clicks count
clicks = 0
running = True

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
            #it is impossible for nightbors_blue == neighbors_red in a birth case, as birth case require neighboring cell = 3
                if neighbors_blue > neighbors_red:
                    new_grid[y][x] = 1
                else:
                    new_grid[y][x] = 2
    grid = new_grid

    if check_criteria.check_dead(grid):
        print("should stop running")
        global running
        running = False

def game_over_display(winner):
    font = pygame.font.Font(None, 36)
    # Draw background
    screen.fill((0, 0, 0))

    # Draw text
    text = font.render(f"{winner}", True, (255, 255, 255))
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
    font = pygame.font.Font(None, 12)
    return_text = font.render("Home", True, (255, 255, 255))
    screen.blit(return_text, (return_button1.x, return_button1.y + 1))

    # Update the display
    pygame.display.flip()

def competition_game():
    # Initialize Pygame
    pygame.init()
    global clicks
    clicks = 0
    global screen
    screen = pygame.display.set_mode((width, height))
    global grid
    grid = np.zeros((rows, cols), dtype=int)  #an array that represents each cell, either 1 or 0 (alive or dead)

    pygame.display.set_caption("Conway's Game of Life - Click to Add Cells")

    # Main loop
    simulation_started = False
    global running
    running = True
    print(running)

    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False #stops running when user quits the program

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                return_button1 = pygame.Rect(30, 30, 20, 20)
                if return_button1.collidepoint(event.pos):
                    print('trigger!!!')
                    return

            if event.type == pygame.MOUSEBUTTONDOWN and not simulation_started: #when the user is still clicking (first 20 clicks to assign colours)
                mouseX, mouseY = pygame.mouse.get_pos()
                gridX, gridY = mouseX // cell_size, mouseY // cell_size
                if grid[gridY][gridX] == 0:  # Check if the cell is not already filled
                    clicks += 1

                    #total of 20 clicks for each colour. First 10 clicks are blue, then next 10 red. The 21st click triggers...
                    #the program to run.

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
        return_button1 = pygame.Rect(30, 30, 20, 20)
        return_button(return_button1)

        pygame.display.flip()
        if simulation_started == True: 
            pygame.time.delay(1000)  # Delay to slow down the simulation

            ## what's the result?
            result = check_criteria.check_competition_winner(grid)
            print(result)
            if result is None:
                continue
            elif result == 1:
                running = False
                game_over_display('User 1 Wins!')
            elif result == 2:
                running = False
                game_over_display('User 2 Wins!')
            else:
                running = False
                game_over_display('TIED!')

    return
    # pygame.quit()