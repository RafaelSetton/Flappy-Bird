import pygame as pg

from .screens import *


class Game:
    DP_HEIGHT = 500
    DP_WIDTH = 1000
    
    @property
    def dp_width(self):
        return self.DP_WIDTH * self.scale

    @property
    def dp_height(self):
        return self.DP_HEIGHT * self.scale

    def __init__(self, scale: float = 1):
        self.scale = scale
        self.tela: pg.Surface = pg.display.set_mode((self.dp_width, self.dp_height))
        self.running = True

    def quit(self):
        self.birds = []
        self.running = False

    def loop(self, fps=80):
        while True:        
            sel_screen = SelectionScreen(self.tela)
            sel_screen.loop()

            game = PlayScreen(self.tela, sel_screen.num_players, sel_screen.use_ai)
            game.loop()
            
            HighScoresScreen(self.tela, game.points).loop()

