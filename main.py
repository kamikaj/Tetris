from settings import *
from drawing import *
import sys
import json
import random
import pygame as pg
from tetris import *
from figure import *
from music_player import *

pg.init()

transition_speed = 0.015      # Im mniejsze, tym wolniejsze przejście
transition = 0.0               # 0.0 = dzień, 1.0 = noc
is_day = True

pg.display.set_caption("Tetris - kamikaj")

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()
SCORE_FILE = "resources/highscore.json"

def pause():
    running = True
    while running:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    running = False
        font = pg.font.SysFont("Courier New", 55)
        pause_text = font.render("PAUSED", True, RED)
        screen.blit(pause_text, (SCREEN_WIDTH - pause_text.get_width(), 20))
        pg.display.flip()

pg.init()

def load_highest_score():
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, 'r') as file:
            try:
                score = json.load(file)
                return score
            except json.JSONDecodeError:
                return 0
    return 0

def save_highest_score(score):
    current_best = load_highest_score()

    if score > current_best:
        with open(SCORE_FILE, 'w') as file:
            json.dump(score, file)

def main():
    running = True
    counter = 0
    pressing_down = False
    intro_screen = True
    is_day = True

    player = MusicPlayer(MUSIC_FOLDER)

    game = Tetris(20, 10)

    while running:
        highest_score = load_highest_score()
        clock.tick(FPS)

        if game.state == 'gameover':
            save_highest_score(game.score)
            player.play_gameover()
            game.gameover(screen, player)

        if intro_screen:
            intro_screen = game.intro_screen(screen, intro_screen, player)

        if game.figure is None:
            game.new_figure()
        counter += 1

        if counter > 100000:
            counter = 0

        if counter % (FPS // game.level // 2) == 0 or pressing_down:
            if game.state == "start":
                game.go_down(screen, player)


        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    game.rotate()
                elif event.key == pg.K_DOWN:
                    pressing_down = True
                elif event.key == pg.K_LEFT:
                    game.go_side(-1)
                elif event.key == pg.K_RIGHT:
                    game.go_side(1)
                elif event.key == pg.K_SPACE:
                    game.go_space(screen, player)
                elif event.key == pg.K_ESCAPE:
                    save_highest_score(game.score)
                    game.__init__(20, 10)
                    intro_screen = True
                elif event.key == pg.K_m:
                    player.play_next()
                elif event.key == pg.K_k:
                    player.end_of_music()
                elif event.key == pg.K_i:
                    pauza(screen)


            elif event.type == pg.KEYUP:
                if event.key == pg.K_DOWN:
                    pressing_down = False


        is_day = update_positions(is_day)
        draw_background(screen, is_day)
        draw_panel_info(screen, game.score, highest_score)

        game.draw_fallen_figures(screen)

        game.draw_falling_figures(screen)

        pg.display.flip()

if __name__ == '__main__':
    main()