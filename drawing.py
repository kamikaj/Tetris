from settings import *
import pygame as pg

def update_positions(is_day):
    global sun_x, moon_x, cloud_x

    cloud_x += 0.5
    if cloud_x > SCREEN_WIDTH:
        cloud_x = -200

    if is_day:
        sun_x += 0.1
        if sun_x > SCREEN_WIDTH + 100:
            moon_x = INFO_PANEL_WIDTH-50
            return False
    else:
        moon_x += 0.1
        if moon_x > SCREEN_WIDTH + 100:
            sun_x = INFO_PANEL_WIDTH-50
            return True

    return is_day

def draw_stars(screen):
    for x, y in stars:
        pg.draw.circle(screen, (255, 255, 255), (x, y), 1)

def draw_sphinx(screen, is_day):
    if is_day:
        SPHINX_COLOR = (222, 184, 135)     # Kolor piaskowy
        SHADOW_COLOR = (184, 134, 90)      # Cień/piasek ciemniejszy
        LINE_COLOR = (0, 0, 0)             # Czarne linie
    else:
         SPHINX_COLOR = (111, 92, 63)  # Kolor piaskowy
         SHADOW_COLOR = (92, 72, 45)  # Cień/piasek ciemniejszy
         LINE_COLOR = (0, 0, 0)  # Czarne linie

    # Podstawowe współrzędne
    base_y = SCREEN_HEIGHT - 50
    body_x = SCREEN_WIDTH // 2 - 130
    body_y = base_y - 40

    # Ciało Sfinksa
    pg.draw.rect(screen, SPHINX_COLOR, (body_x, body_y, 120, 40))  # ciało
    pg.draw.rect(screen, SPHINX_COLOR, (body_x + 10, base_y - 20, 15, 20))  # łapa 1
    pg.draw.rect(screen, SPHINX_COLOR, (body_x + 35, base_y - 20, 15, 20))  # łapa 2

    # Głowa
    head_w = 40
    head_h = 50
    head_x = body_x + 80
    head_y = body_y - head_h + 10

    # Twarz
    pg.draw.rect(screen, SPHINX_COLOR, (head_x, head_y, head_w, head_h))

    # Hełm
    pg.draw.rect(screen, SPHINX_COLOR, (head_x - 10, head_y + 10, 10, 30))
    pg.draw.rect(screen, SPHINX_COLOR, (head_x + head_w, head_y + 10, 10, 30))

    eye_y = head_y + 15
    pg.draw.circle(screen, LINE_COLOR, (head_x + 10, eye_y), 2)
    pg.draw.circle(screen, LINE_COLOR, (head_x + 30, eye_y), 2)

    nose_top = (head_x + 20, eye_y + 2)
    nose_left = (head_x + 17, eye_y + 10)
    nose_right = (head_x + 23, eye_y + 10)
    pg.draw.polygon(screen, LINE_COLOR, [nose_top, nose_left, nose_right])

    mouth_y = eye_y + 20
    pg.draw.line(screen, LINE_COLOR, (head_x + 15, mouth_y), (head_x + 25, mouth_y), 1)

    # Broda faraona
    pg.draw.rect(screen, SHADOW_COLOR, (head_x + 18, head_y + head_h, 4, 10))

def draw_pyramid(screen, is_day):
    if is_day:
        # Kolor piramidy (piaskowy / beżowy)
        PYRAMID_COLOR = (210, 180, 140)
    else:
        PYRAMID_COLOR = (105, 90, 70)

    # Pozycja i wymiary piramidy
    base_y = SCREEN_HEIGHT - 50  # podłoże (nad trawą)
    pyramid_height = 150
    pyramid_width = 200
    center_x = SCREEN_HEIGHT // 2 + 100  # trochę w prawo od środka

    # Wierzchołki trójkąta
    top = (center_x, base_y - pyramid_height)
    bottom_left = (center_x - pyramid_width // 2, base_y)
    bottom_right = (center_x + pyramid_width // 2, base_y)

    # Rysowanie trójkątnej piramidy
    pg.draw.polygon(screen, PYRAMID_COLOR, [top, bottom_left, bottom_right])
    pg.draw.rect(screen, (33, 33, 33), (center_x - 5, base_y - 20, 10, 20))


def draw_background(screen, is_day):
    if is_day:
        screen.fill(LIGHT_SKY_BLUE) #kolor nieba
        pg.draw.circle(screen, ORANGE, (sun_x, 100), 40) #słońce
        pg.draw.rect(screen, YELLOW, (0, SCREEN_HEIGHT-50, SCREEN_WIDTH, 50)) #piasek
    else:
        screen.fill((5, 5, 5)) #kolor nocy
        pg.draw.circle(screen, MOON, (moon_x, 100), 30) #księżyc
        pg.draw.rect(screen, DARK_YELLOW, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50)) #piasek w nocy
        draw_stars(screen) #gwiazdy
    pg.draw.ellipse(screen, DARK_WHITE, (cloud_x, 80, 120, 60))
    pg.draw.ellipse(screen, DARK_WHITE, (cloud_x + 60, 60, 100, 50))

    draw_pyramid(screen, is_day)
    draw_sphinx(screen, is_day)

def draw_panel_info(screen, score, highest_score):
    pg.draw.rect(screen, (LIGHT_PURPLE), (0, 0, INFO_PANEL_WIDTH, SCREEN_HEIGHT))
    pg.draw.rect(screen, (LIGHT_RED), (600, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pg.font.SysFont("Courier New", 33)

    title_surface = font.render("TETRIS", True, LIGHT_SKY_BLUE)
    screen.blit(title_surface, (INFO_PANEL_WIDTH // 2 - title_surface.get_width() // 2, 30))

    font = pg.font.SysFont("Courier New", 24)
    score_surface = font.render(f"Score: {score}", True, ORANGE)
    screen.blit(score_surface, (20, 80))
    score_surface = font.render(f"Highest score:", True, ORANGE)
    screen.blit(score_surface, (5, 700))
    score_surface = font.render(f"{highest_score}", True, ORANGE)
    screen.blit(score_surface, (100, 720))

    font = pg.font.SysFont("Courier New", 18)
    help_lines = [
        " Sterowanie:",
        " ← →  ruch",
        " ↑    obrót",
        " ↓    szybciej",
        "'space'=teleport",
        "m=kolejny utwor",
        "k=brak muzyki",
        "esc=restart"
    ]
    y = 140
    for line in help_lines:
        text_surface = font.render(line, True, TEXT_COLOR)
        screen.blit(text_surface, (20, y))
        y += 30

def pauza(screen):
    running = True
    while running:
        pg.draw.rect(screen, WHITE,(300, 300, 50, 200))
        pg.draw.rect(screen, WHITE, (450, 300, 50, 200))
        font = pg.font.SysFont('Cosmos', 66)
        resume_text = font.render("click i to resume", True, RED)
        screen.blit(resume_text, (SCREEN_WIDTH//2 - resume_text.get_width()//2, SCREEN_HEIGHT - 100))
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit(0)
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_i:
                    running = False