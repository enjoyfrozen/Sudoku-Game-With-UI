import pygame
import os
import ui

# Menu button dimensions
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 60
BUTTON_MARGIN = 20
FONT = pygame.font.Font(None, 40)

# Load the background image
REL_DIR = os.path.dirname(os.path.abspath(__file__))
backgroundImage_PATH = os.path.join(REL_DIR, "assets", "images", "menuBkg.png")

try:
    backgroundImage = pygame.image.load(backgroundImage_PATH).convert()
    backgroundImage = pygame.transform.scale(backgroundImage, (ui.WINDOW_WIDTH, ui.WINDOW_HEIGHT))  # Scale to window size
except FileNotFoundError:
    print(f"Error: Could not find background image at {backgroundImage_PATH}")
    exit()

def draw_backgroundImg():
    ui.screen.blit(backgroundImage, (0,0))

def draw_title():
    title_text = FONT.render("Sudoku Game", True, ui.WHITE)
    ui.screen.blit(title_text, (ui.WINDOW_WIDTH // 2 - title_text.get_width() // 2, 100))

def draw_startButton():
    # Draw Start Button
    start_button = pygame.Rect((ui.WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2, 200), (BUTTON_WIDTH, BUTTON_HEIGHT))
    pygame.draw.rect(ui.screen, ui.LIGHT_BLUE, start_button)
    start_text = FONT.render("Start Game", True, ui.BLACK)
    text_x = start_button.x + BUTTON_WIDTH // 2 - start_text.get_width() // 2
    text_y = start_button.y + BUTTON_HEIGHT // 2 - start_text.get_height() // 2
    ui.screen.blit(start_text, (text_x, text_y))
    
    # Return the button rectangle for interaction
    return start_button

def draw_quitButton():
    # Draw Quit Button
    quit_button = pygame.Rect((ui.WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2, 300), (BUTTON_WIDTH, BUTTON_HEIGHT))
    pygame.draw.rect(ui.screen, ui.LIGHT_BLUE, quit_button)
    quit_text = FONT.render("Quit", True, ui.BLACK)
    text_x = quit_button.x + BUTTON_WIDTH // 2 - quit_text.get_width() // 2
    text_y = quit_button.y + BUTTON_HEIGHT // 2 - quit_text.get_height() // 2
    ui.screen.blit(quit_text, (text_x, text_y))

    # Return the button rectangle for interaction
    return quit_button

def draw_themeButton(isWhiteThemed):
    # Draw Theme Button
    theme_button = pygame.Rect((ui.WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2, 400), (BUTTON_WIDTH, BUTTON_HEIGHT))
    pygame.draw.rect(ui.screen, ui.LIGHT_BLUE, theme_button)
    theme_text = FONT.render("White Theme" if isWhiteThemed else "Dark Theme", True, ui.BLACK)
    text_x = theme_button.x + BUTTON_WIDTH // 2 - theme_text.get_width() // 2
    text_y = theme_button.y + BUTTON_HEIGHT // 2 - theme_text.get_height() // 2
    ui.screen.blit(theme_text, (text_x, text_y))

    # Return the button rectangle for interaction
    return theme_button

def playAgainButton():
    # Draw Play Again Button
    playAgain_button = pygame.Rect((ui.WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2, 200), (BUTTON_WIDTH, BUTTON_HEIGHT))
    pygame.draw.rect(ui.screen, ui.LIGHT_BLUE, playAgain_button)
    playAgain_text = FONT.render("Play Again", True, ui.BLACK)
    text_x = playAgain_button.x + BUTTON_WIDTH // 2 - playAgain_text.get_width() // 2
    text_y = playAgain_button.y + BUTTON_HEIGHT // 2 - playAgain_text.get_height() // 2
    ui.screen.blit(playAgain_text, (text_x, text_y))
    
    # Return the button rectangle for interaction
    return playAgain_button

def draw_difficultyMenu():
    """Draw the difficulty selection menu and return the buttons."""
    title = FONT.render("Select Difficulty", True, ui.WHITE)
    ui.screen.blit(title, (ui.WINDOW_WIDTH // 2 - title.get_width() // 2, 100))

    # Button properties
    BUTTON_WIDTH, BUTTON_HEIGHT = 200, 40
    BUTTON_MARGIN = 20
    difficulties = ["Easy", "Medium", "Hard", "Extreme","Menu"]
    buttons = {}

    for i, diff in enumerate(difficulties):
        button_rect = pygame.Rect(
            ui.WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2, 
            200 + i * (BUTTON_HEIGHT + BUTTON_MARGIN), 
            BUTTON_WIDTH, BUTTON_HEIGHT
        )
        pygame.draw.rect(ui.screen, ui.LIGHT_BLUE, button_rect)
        text = FONT.render(diff, True, ui.BLACK)
        ui.screen.blit(text, (button_rect.centerx - text.get_width() // 2, 
                              button_rect.centery - text.get_height() // 2))
        buttons[diff] = button_rect  # Store button rects with keys

    return buttons