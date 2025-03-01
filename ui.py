import pygame
import os

#Initialize Pygame
pygame.init()

# Get the relative path of the current script
REL_DIR = os.path.dirname(os.path.abspath(__file__))

# Paddings
HORIZONTAL_PAD = 40
VERTICAL_PAD = 40

# Grid Size
GRID_WIDTH, GRID_HEIGHT = 450, 450 # Must be a multiple of 9
GRID_SIZE = 9
CELL_SIZE = GRID_WIDTH // GRID_SIZE

# Grid Margins
GRID_TOP_MARGIN = HORIZONTAL_PAD 
GRID_LEFT_MARGIN = HORIZONTAL_PAD
GRID_RIGHT_MARGIN = GRID_WIDTH + GRID_LEFT_MARGIN
GRID_BOTTOM_MARGIN = GRID_HEIGHT + GRID_TOP_MARGIN

# KeyPad Size
KEYPAD_HEIGHT, KEYPAD_WIDTH = GRID_HEIGHT, 6 * CELL_SIZE + 20

# KeyPad Margins
KEYPAD_TOP_MARGIN = HORIZONTAL_PAD
KEYPAD_LEFT_MARGIN = GRID_BOTTOM_MARGIN + HORIZONTAL_PAD
KEYPAD_RIGHT_MARGIN = KEYPAD_LEFT_MARGIN + KEYPAD_WIDTH
KEYPAD_BOTTOM_MARGIN = KEYPAD_TOP_MARGIN + KEYPAD_HEIGHT

# Window Size
WINDOW_HEIGHT = GRID_HEIGHT + 2 * VERTICAL_PAD
WINDOW_WIDTH = GRID_WIDTH + KEYPAD_WIDTH + 3 * HORIZONTAL_PAD

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (200,200,200)
BLUE = (90,123,192)
LIGHT_BLUE = (173, 216, 230)

#Set up screen
screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Sudoku")

#Set up fonts
gridFont = pygame.font.Font(None,40)


headerFont_PATH = os.path.join(REL_DIR,"assets", "fonts", "Poppins-Bold.ttf")
try:
    headerFont = pygame.font.Font(headerFont_PATH,15)
    newGameFont = pygame.font.Font(headerFont_PATH,25)
except FileNotFoundError:
    print(f"Error: Could not find background image at {headerFont_PATH}")
    exit()


keyPadFont_PATH = os.path.join(REL_DIR,"assets", "fonts", "Achemost.otf")
try:
    keyPadFont = pygame.font.Font(keyPadFont_PATH, 60)
except FileNotFoundError:
    print(f"Error: Could not find background image at {keyPadFont_PATH}")
    exit()


youWinImage_PATH = os.path.join(REL_DIR, "assets", "images", "youWin.png")
try:
    youWinImage = pygame.image.load(youWinImage_PATH).convert()
    youWinImage = pygame.transform.scale(youWinImage, (WINDOW_WIDTH, WINDOW_HEIGHT))  # Scale to window size
except FileNotFoundError:
    print(f"Error: Could not find background image at {youWinImage_PATH}")
    exit()


def pop_youWin():
    """Pop up the You Win! if the grid is completed"""
    screen.blit(youWinImage,(0,0))


def draw_grid():
    """Draw the Sudoku grid with thin and thick lines."""
    for i in range(1, GRID_SIZE):
        # Horizontal lines
        pygame.draw.line(screen, GRAY, (GRID_LEFT_MARGIN,i*CELL_SIZE+GRID_TOP_MARGIN), (GRID_RIGHT_MARGIN, i*CELL_SIZE+GRID_TOP_MARGIN), 1)
        # Vertical lines
        pygame.draw.line(screen, GRAY, (GRID_LEFT_MARGIN + i * CELL_SIZE, GRID_TOP_MARGIN), (GRID_LEFT_MARGIN + i * CELL_SIZE, GRID_BOTTOM_MARGIN), 1)

    # Draw thick lines for the 3x3 sub-grids
    for i in range(0, GRID_SIZE+1,3):
        # Horizontal lines
        pygame.draw.line(screen, BLACK, (GRID_LEFT_MARGIN,i*CELL_SIZE+GRID_TOP_MARGIN), (GRID_RIGHT_MARGIN, i*CELL_SIZE+GRID_TOP_MARGIN), 2)
        # Vertical lines
        pygame.draw.line(screen, BLACK, (GRID_LEFT_MARGIN + i * CELL_SIZE, GRID_TOP_MARGIN), (GRID_LEFT_MARGIN + i * CELL_SIZE, GRID_BOTTOM_MARGIN), 2)
        


def draw_numbers(grid, puzzle):
    """Draw the numbers in the Sudoku grid."""
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] != 0 and grid[row][col] == puzzle[row][col]:
                num = gridFont.render(str(grid[row][col]), True, BLACK)
                text_x = (col+0.5) * CELL_SIZE + GRID_LEFT_MARGIN - num.get_width() // 2
                text_y = (row+0.5) * CELL_SIZE + GRID_TOP_MARGIN - num.get_height() // 2
                screen.blit(num, (text_x, text_y))
            elif grid[row][col] != 0 and grid[row][col] != puzzle[row][col]:
                num = gridFont.render(str(grid[row][col]), True, BLUE)
                text_x = (col+0.5) * CELL_SIZE + GRID_LEFT_MARGIN - num.get_width() // 2
                text_y = (row+0.5) * CELL_SIZE + GRID_TOP_MARGIN - num.get_height() // 2
                screen.blit(num, (text_x, text_y))


def draw_header(start_time, difficulty):
    """Draw the timer and the difficulty above the grid."""
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    minutes, seconds = divmod(elapsed_time, 60)

    # Render timer and difficulty separately
    timer_text = headerFont.render(f"Time: {minutes:02}:{seconds:02}", True, BLACK)
    difficulty_text = headerFont.render(f"Difficulty: {difficulty}", True, BLACK)

    # Fixed positions
    timer_x = GRID_LEFT_MARGIN  # Align to the left
    timer_y = VERTICAL_PAD // 2 - timer_text.get_height() // 2
    difficulty_x = GRID_LEFT_MARGIN + GRID_WIDTH - difficulty_text.get_width()  # Align to the right
    difficulty_y = VERTICAL_PAD // 2 - difficulty_text.get_height() // 2

    # Draw both texts at fixed positions
    screen.blit(timer_text, (timer_x, timer_y))  # Timer on the left
    screen.blit(difficulty_text, (difficulty_x, difficulty_y))  # Difficulty on the right


def draw_newGame():
    """Draw a high-resolution 'New Game' button with smooth edges and return its rectangle."""
    #Creating High Resolution Surface for round edges
    newgame_width = (KEYPAD_WIDTH // 2)
    scale_factor = 4  # Scale up by 4x
    high_res_width = newgame_width * scale_factor
    high_res_height = CELL_SIZE * scale_factor
    high_res_surface = pygame.Surface((high_res_width, high_res_height), pygame.SRCALPHA)

    # Draw the high-resolution rounded rectangle
    corner_radius = 20 * scale_factor
    pygame.draw.rect(high_res_surface, BLUE, (0, 0, high_res_width, high_res_height), border_radius=corner_radius)

    # Scale down and blit the button
    smooth_surface = pygame.transform.smoothscale(high_res_surface, (newgame_width, CELL_SIZE))
    button_x = KEYPAD_RIGHT_MARGIN - KEYPAD_WIDTH // 2
    button_y = KEYPAD_BOTTOM_MARGIN - high_res_height / scale_factor - CELL_SIZE - 10
    
    screen.blit(smooth_surface, (button_x,button_y))

    # Draw "New Game" text
    newGame_text = newGameFont.render("New Game", True, WHITE)
    text_x = button_x + newgame_width // 2 - newGame_text.get_width() // 2
    text_y = button_y + CELL_SIZE // 2 - newGame_text.get_height() // 2
    screen.blit(newGame_text, (text_x, text_y))

    # Return the button rectangle for interaction
    return pygame.Rect(button_x,button_y, newgame_width,CELL_SIZE)

def draw_reset():
    """Draw a high-resolution 'Reset' button with smooth edges and return its rectangle."""
    #Creating High Resolution Surface for round edges
    scale_factor = 4  # Scale up by 4x
    high_res_width = (KEYPAD_WIDTH // 2.5) * scale_factor
    high_res_height = CELL_SIZE * scale_factor
    high_res_surface = pygame.Surface((high_res_width, high_res_height), pygame.SRCALPHA)

    # Draw the high-resolution rounded rectangle
    corner_radius = 20 * scale_factor
    pygame.draw.rect(high_res_surface, BLUE, (0, 0, high_res_width, high_res_height), border_radius=corner_radius)

    # Scale down and blit the button
    smooth_surface = pygame.transform.smoothscale(high_res_surface, ((KEYPAD_WIDTH // 2.5), CELL_SIZE))
    button_x = KEYPAD_LEFT_MARGIN
    button_y = KEYPAD_BOTTOM_MARGIN - high_res_height / scale_factor
    screen.blit(smooth_surface, (button_x,button_y))

    # Draw "Reset" text
    clear_text = newGameFont.render("Reset", True, WHITE)
    text_x = button_x + KEYPAD_WIDTH // 5 - clear_text.get_width() // 2
    text_y = button_y + CELL_SIZE // 2 - clear_text.get_height() // 2
    screen.blit(clear_text, (text_x, text_y))

    # Return the button rectangle for interaction
    return pygame.Rect(button_x,button_y,(KEYPAD_WIDTH // 2.5),CELL_SIZE)

def draw_keypad():
    """Draws the keypad and returns a list of button rectangles with their values."""
    buttons = [] # List to store buttons and their values
    for i in range (1, 10):
        # Creating High Resolution Surface for round edges
        scale_factor = 4  # Scale up by 4x
        high_res_width = 2 * CELL_SIZE * scale_factor
        high_res_height = 2 * CELL_SIZE * scale_factor
        high_res_surface = pygame.Surface((high_res_width, high_res_height), pygame.SRCALPHA)

        # Draw the high-resolution rounded rectangle
        corner_radius = 20 * scale_factor
        pygame.draw.rect(high_res_surface, LIGHT_BLUE, (0, 0, high_res_width, high_res_height), border_radius=corner_radius)

        # Scale down and blit the button
        smooth_surface = pygame.transform.smoothscale(high_res_surface, (2 * CELL_SIZE, 2 * CELL_SIZE))
        button_x = KEYPAD_LEFT_MARGIN + ((i-1)%3)*(2*CELL_SIZE + 10)
        button_y = KEYPAD_TOP_MARGIN + ((i-1)//3)*(2*CELL_SIZE + 10)
            
        screen.blit(smooth_surface, (button_x,button_y))

        # Draw the number text
        keyPad_text = keyPadFont.render(f"{i}", True, BLUE)
        text_x = button_x + CELL_SIZE - keyPad_text.get_width() // 2
        text_y = button_y + CELL_SIZE - keyPad_text.get_height() // 2 + 5
        screen.blit(keyPad_text, (text_x, text_y))

        #Add the button rectangle and its value to the list
        button_rect = pygame.Rect(button_x,button_y, 2 * CELL_SIZE, 2 * CELL_SIZE)
        buttons.append((button_rect, i)) #Tuple of (rectangle, value)
    return buttons # Return the list of buttons

def draw_returnMenu():
    """Draw a high-resolution 'Main Menu' button with smooth edges and return its rectangle."""
    #Creating High Resolution Surface for round edges
    scale_factor = 4  # Scale up by 4x
    high_res_width = (KEYPAD_WIDTH // 2) * scale_factor
    high_res_height = CELL_SIZE * scale_factor
    high_res_surface = pygame.Surface((high_res_width, high_res_height), pygame.SRCALPHA)

    # Draw the high-resolution rounded rectangle
    corner_radius = 20 * scale_factor
    pygame.draw.rect(high_res_surface, BLUE, (0, 0, high_res_width, high_res_height), border_radius=corner_radius)

    # Scale down and blit the button
    smooth_surface = pygame.transform.smoothscale(high_res_surface, ((KEYPAD_WIDTH // 2), CELL_SIZE))
    button_x = KEYPAD_RIGHT_MARGIN - KEYPAD_WIDTH // 2
    button_y = KEYPAD_BOTTOM_MARGIN - high_res_height / scale_factor
    screen.blit(smooth_surface, (button_x,button_y))

    # Draw "Main Menu" text
    returnMenu_text = newGameFont.render("Main Menu", True, WHITE)
    text_x = button_x + KEYPAD_WIDTH // 4 - returnMenu_text.get_width() // 2
    text_y = button_y + CELL_SIZE // 2 - returnMenu_text.get_height() // 2
    screen.blit(returnMenu_text, (text_x, text_y))

    # Return the button rectangle for interaction
    return pygame.Rect(button_x,button_y,(KEYPAD_WIDTH // 2),CELL_SIZE)

def draw_clear():
    """Draw a high-resolution 'Erase' button with smooth edges and return its rectangle."""
    #Creating High Resolution Surface for round edges
    scale_factor = 4  # Scale up by 4x
    high_res_width = (KEYPAD_WIDTH // 2.5) * scale_factor
    high_res_height = CELL_SIZE * scale_factor
    high_res_surface = pygame.Surface((high_res_width, high_res_height), pygame.SRCALPHA)

    # Draw the high-resolution rounded rectangle
    corner_radius = 20 * scale_factor
    pygame.draw.rect(high_res_surface, BLUE, (0, 0, high_res_width, high_res_height), border_radius=corner_radius)

    # Scale down and blit the button
    smooth_surface = pygame.transform.smoothscale(high_res_surface, ((KEYPAD_WIDTH // 2.5), CELL_SIZE))
    button_x = KEYPAD_LEFT_MARGIN
    button_y = KEYPAD_BOTTOM_MARGIN - high_res_height / scale_factor - CELL_SIZE - 10
    screen.blit(smooth_surface, (button_x,button_y))

    # Draw "Erase" text
    clear_text = newGameFont.render("Erase", True, WHITE)
    text_x = button_x + KEYPAD_WIDTH // 5 - clear_text.get_width() // 2
    text_y = button_y + CELL_SIZE // 2 - clear_text.get_height() // 2
    screen.blit(clear_text, (text_x, text_y))

    # Return the button rectangle for interaction
    return pygame.Rect(button_x,button_y,(KEYPAD_WIDTH // 2.5),CELL_SIZE)


def highLight_cell(selected_cell):
    """Highlight a selected cell on the grid."""
    (row,col) = selected_cell
    cell_x = col * CELL_SIZE + GRID_LEFT_MARGIN
    cell_y = row * CELL_SIZE + GRID_LEFT_MARGIN

    # Draw a slightly thicker rectangle to highlight the cell
    highlight_color = (90, 123, 192, 100)  # Semi-transparent blue
    highlight_surface = pygame.Surface((CELL_SIZE,CELL_SIZE), pygame.SRCALPHA)
    highlight_surface.fill(highlight_color)

    screen.blit(highlight_surface, (cell_x, cell_y))
	
def mark_cell(selected_cell, bMark):
    """Highlight a selected cell on the grid."""
    (row,col) = selected_cell
    cell_x = col * CELL_SIZE + GRID_LEFT_MARGIN
    cell_y = row * CELL_SIZE + GRID_LEFT_MARGIN

    # Draw a slightly thicker rectangle to highlight the cell
    if bMark:
        highlight_color = BLUE  # Semi-transparent blue #82 橙红色 #FF2400 #https://www.cnblogs.com/ybqjymy/p/18027171
    else:
        highlight_color = LIGHT_BLUE  # Semi-transparent blue #82 橙红色 #FF2400 #https://www.cnblogs.com/ybqjymy/p/18027171
	
    highlight_surface = pygame.Surface((CELL_SIZE,CELL_SIZE), pygame.SRCALPHA)
    pygame.draw.rect(highlight_surface, highlight_color, (0, 0, CELL_SIZE, CELL_SIZE))
    #highlight_surface.fill(highlight_color)

    screen.blit(highlight_surface, (cell_x, cell_y))	

def toggleDarkTheme(isWhiteThemed):
    """Toggles between white and dark theme"""
    global WHITE, BLACK, GRAY, BLUE, LIGHT_BLUE  # Declare all as global

    if isWhiteThemed:
        # Set Dark Theme Colors
        WHITE = (200, 200, 200)       # Soft off-white for text/numbers
        BLACK = (15, 15, 20)          # Very dark gray for the background
        GRAY = (50, 50, 60)           # Dark gray for grid lines
        BLUE = (60, 130, 180)         # Muted blue for numbers/highlights
        LIGHT_BLUE = (40, 90, 130)    # Dark desaturated blue for buttons/selection
    else:
        # Set White Theme Colors
        WHITE = (255,255,255)
        BLACK = (0,0,0)
        GRAY = (200,200,200)
        BLUE = (90,123,192)
        LIGHT_BLUE = (173, 216, 230)
    return not isWhiteThemed

def didWin(grid,solution):
    """Check if the player's grid matches the solution grid."""
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if(grid[row][col] != solution[row][col]):
                return False
    return True