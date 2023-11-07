import numpy as np

def check_stabilization(grid, new_grid):
    return np.array_equal(grid, new_grid)

def check_dead(grid):
    return np.sum(grid) <= 0

def check_competition_winner(grid):
    print(np.sum(grid == 2))
    # Check if there are only 0's left in the grid, it has to be the 1st 
    if np.sum(grid) == 0:
        return 0
    # Check if there are no 2's left in the grid
    elif np.sum(grid == 2) == 0:
        return 1
    # Check if there are no 1's left in the grid
    elif np.sum(grid == 1) == 0:
        return 2
    # If none of the above conditions are met, return None
    else:
        return None

