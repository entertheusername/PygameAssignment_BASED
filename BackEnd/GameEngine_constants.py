# This file is for storing constants game-wide

# Colors
class Colors:
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)

# Game Settings
class GameSettings:
    WIDTH, HEIGHT = 1080, 640
    BASKET_WIDTH, BASKET_HEIGHT = 128, 128
    APPLE_RADIUS = 64
    SPEED = 5

WIDTH = GameSettings.WIDTH
HEIGHT = GameSettings.HEIGHT
APPLE_RADIUS = GameSettings.APPLE_RADIUS