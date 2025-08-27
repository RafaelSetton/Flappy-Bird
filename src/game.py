import json
import pygame as pg
from os import remove, makedirs

from src.screens.savescores import SaveScores

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
            sel_screen.loop(fps)

            game = PlayScreen(self.tela, sel_screen.num_players, sel_screen.use_ai)
            game.loop(fps)

            with open('data/highscores.json', 'r') as f:
                high_scores = json.load(f)
                min_score = min(high_scores.values(), default=0)

            makedirs('data', exist_ok=True)
            with open('data/newscores.json', 'r') as f:
                scores = json.load(f)
                for player, points in scores.items():
                    if points <= min_score:
                        continue
                    high_scores = SaveScores(self.tela, player, points)
                    high_scores.loop(fps)
            remove('data/newscores.json')
            
            HighScoresScreen(self.tela, game.points).loop(fps)

