from figure import *
from settings import *
import pygame as pg


class Tetris:
    def __init__(self, height, width):
        self.level = 2
        self.score = 0
        self.state = "start"
        self.field = []
        self.height = 0
        self.width = 0
        self.x = INFO_PANEL_WIDTH
        self.y = 0
        self.zoom = 40
        self.figure = None

        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        self.point_sound = pg.mixer.Sound("resources/music/point_sound.mp3")
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self):
        self.figure = Figure(3, 0)

    def intersects(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    y = i + self.figure.y
                    x = j + self.figure.x
                    if y > self.height - 1 or x > self.width - 1 or x < 0:
                        return True
                    if self.field[y][x] > 0:
                        return True
        return False

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2
        self.point_sound.play()

    def go_space(self, screen, player):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze(screen, player)

    def go_down(self, screen, player):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze(screen, player)

    def freeze(self, screen, player):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation

    def gameover(self, screen, player):
        running = True
        while running:
            for i in range(self.height):
                for j in range(self.width):
                    pg.draw.rect(screen, BLACK, [self.x + self.zoom * j, self.y + self.zoom * i, self.zoom, self.zoom],
                                 1)
                    if self.field[i][j] > 0:
                        pass
                        pg.draw.rect(screen, BLACK,
                                     [self.x + self.zoom * j + 1, self.y + self.zoom * i + 1, self.zoom - 2,
                                      self.zoom - 1])

            self.draw_falling_figures(screen)

            font = pg.font.SysFont('Cosmos', 55)

            gameover_text = font.render("GAME OVER", True, RED)
            screen.blit(gameover_text, (SCREEN_WIDTH//2 - gameover_text.get_width()//2,
                                        SCREEN_HEIGHT//2 - gameover_text.get_height()//2))

            font = pg.font.SysFont('Cosmos', 33)
            esc_text = font.render(" press ESC to restart", True, RED)
            screen.blit(esc_text, (SCREEN_WIDTH//2 - esc_text.get_width()//2,
                                   SCREEN_HEIGHT//2 - esc_text.get_height()//2 + 50))

            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    pg.quit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running = False
                        self.__init__(20, 10)
                        self.intro_screen(screen, False, player)

    def intro_screen(self, screen, intro_screen, player):
        running = True
        sky_path = "resources/background/pyramids.jpg"
        intro_photo = pg.image.load(sky_path).convert()  # convert() dla szybszego blitowania
        intro_photo = pg.transform.scale(intro_photo, (1.92 * SCREEN_WIDTH, 1.08 * SCREEN_HEIGHT))
        player.play_intro()
        while running:
            screen.blit(intro_photo, (-200, 0))

            font = pg.font.SysFont('Cosmos', 66)

            intro_text = font.render("TETRIS", True, ORANGE)
            screen.blit(intro_text, (SCREEN_WIDTH // 2 - intro_text.get_width() // 2,
                                        SCREEN_HEIGHT // 2 - intro_text.get_height() // 2 - 100))

            font = pg.font.SysFont('Cosmos', 47)
            esc_text = font.render(" press space to start", True, ORANGE)
            screen.blit(esc_text, (SCREEN_WIDTH // 2 - esc_text.get_width() // 2,
                                   SCREEN_HEIGHT // 2 - esc_text.get_height() // 2))

            kamikaj_text = font.render("made by kamikaj", True, BLACK)
            screen.blit(kamikaj_text, (SCREEN_WIDTH // 2 - kamikaj_text.get_width() // 2 + 200,
                                   SCREEN_HEIGHT // 2 - kamikaj_text.get_height() // 2 + 300))

            pg.draw.rect(screen, YELLOW, (SCREEN_WIDTH // 2 - 60 ,
                                          SCREEN_HEIGHT // 2 + 105,
                                          120,
                                          40))
            pg.draw.rect(screen, YELLOW, (SCREEN_WIDTH // 2 - 20,
                                          SCREEN_HEIGHT // 2 + 65,
                                          40,
                                          40))

            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    pg.quit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        player.play_next()
                        running = False

    def draw_fallen_figures(self, screen):
        if self.state == "gameover":
            color = BLACK
        else:
            color = WHITE
        for i in range(self.height):
            for j in range(self.width):
                pg.draw.rect(screen, color, [self.x + self.zoom * j, self.y + self.zoom * i, self.zoom, self.zoom],
                                 1)
                if self.field[i][j] > 0:
                    pass
                    pg.draw.rect(screen, colors[self.field[i][j]],
                                     [self.x + self.zoom * j + 1, self.y + self.zoom * i + 1, self.zoom - 2,
                                         self.zoom - 1])

    def draw_falling_figures(self, screen):
        if self.state == 'gameover':
            self.figure.color = BLACK

        if self.figure is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in self.figure.image():
                        pg.draw.rect(screen, YELLOW,
                                        [self.x + self.zoom * (j + self.figure.x) + 1,
                                            self.y + self.zoom * (i + self.figure.y) + 1,
                                            self.zoom - 2, self.zoom - 2])

    def pauza(self, screen):
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