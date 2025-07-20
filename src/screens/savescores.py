from .base import BaseScreen
import json
import pygame as pg

class SaveScores(BaseScreen):
    def __init__(self, screen, color, score):
        super().__init__(screen)
        self.color = color
        self.score = score
        self.name = ""

    def render(self, frame_n: int, fps: int):
        self.screen.fill((0, 0, 0))
        
        self.draw_text(f"Type name for {self.color} player ({self.score} pts)", 60, color=self.color)
        self.draw_text(self.name, 120)
        
        pg.display.flip()
    
    def event_handler(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    if self.name.strip() == "":
                        self.name = "Anonymous"
                    self.name = self.name.strip()[:20]
                    self.save_scores()
                    self.quit()
                elif event.key == pg.K_BACKSPACE:
                    self.name = self.name[:-1]
                else:
                    self.name += event.unicode

    def save_scores(self):
        with open('data/highscores.json', 'r') as f:
            scores = json.load(f)

        while scores.get(self.name) is not None:
            self.name += " "
        scores[self.name] = self.score
        
        while len(scores) > 20:
            min_score = min(scores.values())
            min_player = [k for k, v in scores.items() if v == min_score][0]
            del scores[min_player]

        with open('data/highscores.json', 'w') as f:
            json.dump(scores, f, indent=4)
