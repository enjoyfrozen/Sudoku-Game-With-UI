import pygame
from sudoku import generate_puzzle, solve, is_valid
import ui
import menu as mn
import os

# States for the game
STATE_MENU = "menu"
STATE_GAME = "game"
STATE_QUIT = "quit"
STATE_OPTIONS = "options"
STATE_WIN = "win"
STATE_NEWGAME = "newgame"

difficulty = ""

# Initialize Pygame and Mixer for Audio
pygame.init()
pygame.mixer.init()

# Load background music
REL_DIR = os.path.dirname(os.path.abspath(__file__))
background_music_path = os.path.join(REL_DIR, "assets", "sounds", "background_music.mp3")

try:
    pygame.mixer.music.load(background_music_path)  # Load the music
    pygame.mixer.music.set_volume(0.01)  # Set volume (0.0 to 1.0)
    pygame.mixer.music.play(-1)  # Loop the music indefinitely
except FileNotFoundError:
    print(f"Error: Could not find background music at {background_music_path}")

def main():
    state = STATE_MENU  # Start in the main menu state
    running = True
    selected_cell = None
    isWhiteThemed = True

    while running:
        # Clear the screen
        ui.screen.fill(ui.WHITE)

        if state == STATE_MENU:
            # Menu State
            mn.draw_backgroundImg()
            mn.draw_title()

            start_button = mn.draw_startButton()
            quit_button = mn.draw_quitButton()
            theme_button = mn.draw_themeButton(isWhiteThemed)

            # Event handling for menu
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if start_button.collidepoint(mouse_pos):
                        state = STATE_OPTIONS  # Switch to options state
                    elif quit_button.collidepoint(mouse_pos):
                        running = False
                    elif theme_button.collidepoint(mouse_pos):
                        isWhiteThemed = ui.toggleDarkTheme(isWhiteThemed)

        elif state == STATE_OPTIONS:
            # Difficulty Selection Menu
            mn.draw_backgroundImg()
            buttons = mn.draw_difficultyMenu()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for diff, button_rect in buttons.items():
                        if button_rect.collidepoint(mouse_pos):
                            difficulty = diff  # Set the selected difficulty
                            if(difficulty!="Menu"):
                                puzzle = generate_puzzle(difficulty)
                                solution = [row[:] for row in puzzle]
                                solve(solution)  # Solve the solution grid completely
                                grid = [row[:] for row in puzzle]
                                state = STATE_GAME  # Play
                                start_time = pygame.time.get_ticks()
                            else:
                                state = STATE_MENU
        elif state == STATE_NEWGAME:
            puzzle = generate_puzzle(difficulty)
            solution = [row[:] for row in puzzle]
            solve(solution)  # Solve the solution grid completely
            grid = [row[:] for row in puzzle]
            state = STATE_GAME  # Play
            start_time = pygame.time.get_ticks()
        elif state == STATE_GAME:
            # Game State
            ui.draw_grid()
            ui.draw_numbers(grid, puzzle)
            ui.draw_header(start_time, difficulty)
            newGame_rect = ui.draw_newGame()
            keyPad_buttons = ui.draw_keypad()
            returnMenu_button = ui.draw_returnMenu()
            clear_button = ui.draw_clear()
            if selected_cell:
                ui.highLight_cell(selected_cell)

            # Event handling for game
            for event in pygame.event.get():	

                # 获取键盘输入
                keys = pygame.key.get_pressed()				
			
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    # Zorro: Add keydown of number support			
                    print(f"Key '{pygame.key.name(event.key)}' pressed", event.key, pygame.K_1, pygame.K_9, pygame.K_KP1, pygame.K_KP9)	
                    value = 0 					
                    if keys[pygame.K_1] or keys[pygame.K_KP1]:
                        value = 1
                    elif keys[pygame.K_2] or keys[pygame.K_KP2]:
                        value = 2
                    elif keys[pygame.K_3] or keys[pygame.K_KP3]:
                        value = 3
                    elif keys[pygame.K_4] or keys[pygame.K_KP4]:
                        value = 4
                    elif keys[pygame.K_5] or keys[pygame.K_KP5]:
                        value = 5
                    elif keys[pygame.K_6] or keys[pygame.K_KP6]:
                        value = 6
                    elif keys[pygame.K_7] or keys[pygame.K_KP7]:
                        value = 7
                    elif keys[pygame.K_8] or keys[pygame.K_KP8]:
                        value = 8
                    elif keys[pygame.K_9] or keys[pygame.K_KP9]:
                        value = 9
                    if value>0:
                        print ("selected_cell",selected_cell, "event.key",event.key,"key value", value)
                        if selected_cell:
                            row, col = selected_cell
                            # Only allow updates on empty cells
                            if puzzle[row][col] == 0 and is_valid(grid, row, col, value):
                                grid[row][col] = value
                                #zorro reserver the selected cell									
                                #selected_cell = None  # Deselect cell after updating
                                # Check if win game
                                if(ui.didWin(grid,solution)):
                                    state = STATE_WIN
                    elif keys[pygame.K_DELETE]:
                        print ("selected_cell",selected_cell, "event.key",event.key,"key value", value)
                        if selected_cell:
                            row, col = selected_cell
                            # Only allow updates on empty cells
                            if puzzle[row][col] == 0:
                                grid[row][col] = 0							
							
                elif event.type == pygame.KEYUP:
                    # Zorro: Add keydown of number support			
                    #print(f"Key '{pygame.key.name(event.key)}' released")										
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Check if "Main Menu" button is clicked
                    if returnMenu_button.collidepoint(mouse_pos):
                        state = STATE_MENU
                    # Check if "New Game" button is clicked
                    if newGame_rect.collidepoint(mouse_pos):
                        state = STATE_NEWGAME #zorro change STATE_OPTIONS to STATE_NEWGAME for "new game" without option change, and using old difficulty

                    # Check if a grid cell is clicked
                    row = (mouse_pos[1] - ui.GRID_TOP_MARGIN) // ui.CELL_SIZE
                    col = (mouse_pos[0] - ui.GRID_LEFT_MARGIN) // ui.CELL_SIZE
                    if 0 <= row < ui.GRID_SIZE and 0 <= col < ui.GRID_SIZE:
                        selected_cell = (row, col)

                    # Check if any keypad button is clicked
                    for button_rect, value in keyPad_buttons:
                        if button_rect.collidepoint(mouse_pos):
                            if selected_cell:
                                row, col = selected_cell
                                # Only allow updates on empty cells
                                if puzzle[row][col] == 0 and is_valid(grid, row, col, value):
                                    grid[row][col] = value
                                    #zorro reserver the selected cell									
                                    #selected_cell = None  # Deselect cell after updating
                                    # Check if win game
                                    if(ui.didWin(grid,solution)):
                                        state = STATE_WIN

                    # Check if "Clear" button is clicked
                    if clear_button.collidepoint(mouse_pos):
                        if selected_cell:
                            row, col = selected_cell
                            # Only allow updates on originally empty cells
                            if puzzle[row][col] == 0:
                                grid[row][col] = 0
                                selected_cell = None # Deselect cell after updating
        elif state == STATE_WIN:
            ui.pop_youWin()
            quit_button = mn.draw_quitButton()
            playAgain_button = mn.playAgainButton()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if quit_button.collidepoint(mouse_pos):
                        running = False
                    elif playAgain_button.collidepoint(mouse_pos):
                        state = STATE_OPTIONS

        # Update the display
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()