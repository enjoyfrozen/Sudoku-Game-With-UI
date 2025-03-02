#Contribute from Serban-Mihail Cora, Zorro

import random

def solve(grid):
    """Solve the sudoku grid"""
    for row in range(9):
        for col in range(9):
            if grid[row][col]==0: #Empty Cell
                numbers = list(range(1, 10))  # Create numbers 1-9
                random.shuffle(numbers)  # Shuffle the numbers to randomize the order
                for num in numbers:
                    if is_valid(grid,row,col,num):
                        grid[row][col]=num
                        if solve(grid):
                            return True
                        grid[row][col]=0 #Backtrack
                return False
    return True

def is_valid(grid, row, col, num):
    """Check if a number is valid in a given position."""
    # Check row, col, 3x3 sub-grid
    if num in grid[row]:
        return False
    if num in [grid[i][col] for i in range (9)]:
        return False
    sub_row, sub_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(sub_row, sub_row + 3):
        for j in range(sub_col, sub_col + 3):
            if grid[i][j] == num:
                return False
    return True

def generate_puzzle(difficulty="easy"):
    """Generate a Sudoku puzzle."""
    grid = [[0] * 9 for _ in range(9)]
    bSolved = False
    while not bSolved:
        bSolved = solve(grid)  # Fill the grid completely
    clues = {"Easy": 40, "Medium": 30, "Hard": 20, "Extreme": 10}[difficulty]
    remove_cells(grid, 81 - clues)
    return grid

def remove_cells(grid, count):
    """Remove cells to create a Sudoku puzzle."""
    while count>0:
        row, col = random.randint(0,8), random.randint(0,8)
        if grid[row][col] != 0:
            grid[row][col] = 0
            count -= 1

