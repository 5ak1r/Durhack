import pygame
import numpy as np
from constants import * 
# Initialize Pygame
pygame.init()



# Cell size and grid

rows, cols = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
grid = np.zeros((rows, cols), dtype=int)  #an array that represents each cell, either 1 or 0 (alive or dead)
print(grid.shape)


# Setting up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life - Click to Add Cells")
# Create font
font = pygame.font.Font(None, 30)

# Create buttons
start_button1 = pygame.Rect(50, 50, 210, 40)
start_button2 = pygame.Rect(50, 100, 250, 40)
quit_button = pygame.Rect(50, 150, 200, 40)


# Main loop
running = True
simulation_started = False
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        # Quit the game if the user closes the screen
        if event.type == pygame.QUIT:
            running = False
        # Handle mouse button down event
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if start_button1.collidepoint(event.pos):
                    import original_mode
                    original_mode.original_game()
                elif start_button2.collidepoint(event.pos):
                    print('enter!!')
                    import competition_mode
                    competition_mode.competition_game()
                elif quit_button.collidepoint(event.pos):
                    print("Quit button clicked")
                    running = False
    # Draw buttons
    pygame.draw.rect(screen, (173, 216, 230), start_button1)
    pygame.draw.rect(screen, (144, 238, 144), start_button2)
    pygame.draw.rect(screen, (0, 255, 0), quit_button)

    # Draw button text
    start_text1 = font.render("Original Game Mode", True, (255, 255, 255))
    screen.blit(start_text1, (start_button1.x, start_button1.y+10))
    start_text2 = font.render("Competition Game Mode", True, (255, 255, 255))
    screen.blit(start_text2, (start_button2.x, start_button2.y+12))
    quit_text = font.render("Quit", True, (255, 255, 255))
    screen.blit(quit_text, (quit_button.x + 50, quit_button.y + 10))


    pygame.display.flip()
    # pygame.time.delay(300)  # Delay to slow down the simulation
pygame.quit()


