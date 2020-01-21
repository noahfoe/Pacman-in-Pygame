from pygame.math import Vector2 as vec
# Game Settings
TOP_BOTTOM_BUFFER = 50

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (107, 107, 107)
YELLOW = (255, 255, 0)
GOLD = (124, 123, 7)
PINK = (255, 192, 203)
ORANGE = (255, 165, 0)


# display
WIDTH = 610
HEIGHT = 670
MAZE_WIDTH, MAZE_HEIGHT = WIDTH-TOP_BOTTOM_BUFFER, HEIGHT-TOP_BOTTOM_BUFFER
ROWS = 30
COLS = 28
# FPS
FPS = 60

# player settings
PLAYER_START_POS = 0

# menu settings
MENU_TEXT_SIZE = 16
MENU_TEXT_COLOR = (170, 132, 58)
MENU_FONT = 'arial black'