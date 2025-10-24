import os
import pygame as pg
from settings import MUSIC_FOLDER

class MusicPlayer:
    def __init__(self, folder):
        self.tracks = [
            os.path.join(folder, f)
            for f in os.listdir(folder)
            if f.endswith((".mp3", ".ogg", ".wav"))
        ]
        self.tracks.sort()  # odtwarzanie w kolejności nazw plików
        self.index = 0

        pg.mixer.init()
        pg.mixer.music.set_endevent(pg.USEREVENT + 1)  # event po skończeniu utworu

    def play_next(self):
        if not self.tracks:
            return
        track = self.tracks[self.index]
        print(f"Odtwarzam: {os.path.basename(track)}")
        pg.mixer.music.load(track)
        pg.mixer.music.play()
        self.index = (self.index + 1) % len(self.tracks)  # pętla w kółko

    def handle_event(self, event):
        if event.type == pg.USEREVENT + 1:  # koniec utworu
            self.play_next()

    def play_intro(self):
        print("Odtwarzam intro")
        pg.mixer.music.load('resources/music/01 - Intro.mp3')
        pg.mixer.music.play()

    def play_gameover(self):
        print("Odtwarzam gameover")
        pg.mixer.music.load('resources/music/gameover_sound.mp3')
        pg.mixer.music.play()

    def end_of_music(self):
        pg.mixer.music.stop()