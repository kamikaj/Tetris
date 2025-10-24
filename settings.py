import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
INFO_PANEL_WIDTH = SCREEN_WIDTH / 4
FPS = 60
MUSIC_FOLDER = "C:/Users/User/PycharmProjects/Tetris/resources/music/soundtrack/"

#Colors
WHITE = (255, 255, 255)
DARK_WHITE = (200, 200, 200)
PURPLE = (50, 0, 50)
LIGHT_PURPLE = (70, 25, 100)
LIGHT_SKY_BLUE = (135, 206, 250)
ORANGE = (255, 165, 0)
TEXT_COLOR = (235, 236, 230)
MOON = (248, 248, 248)
YELLOW = (200, 200, 0)
DARK_YELLOW = (100, 100, 0)
DAY_COLOR = (135,206,250)
NIGHT_COLOR = (5, 5, 5)
RED = (255, 0, 0)
LIGHT_RED = (155, 25, 25)
BLACK = (0, 0, 0)

# Pozycje
sun_x = INFO_PANEL_WIDTH-50
moon_x = SCREEN_WIDTH
cloud_x = 0
stars = [(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT // 2)) for _ in range(50)]