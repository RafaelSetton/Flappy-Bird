from typing import List
import pygame as pg
import json

from .base import BaseScreen


class HighScoresScreen(BaseScreen):
    def __init__(self, screen, *args):
        super().__init__(screen)

    def place_text(self, text: pg.Surface, dy: int):
        dx = (self.screen.get_width() - text.get_width()) / 2 
        self.screen.blit(text, (dx, dy))

    def render(self, frame_n: int, fps: int):
        try:
            with open("./data/highscores.json", "r") as f:
                data = json.load(f)
        except Exception as e:
            print(f"Failed to load high scores: {e}")
            return

        # Sort scores descending
        sorted_scores = sorted(data.items(), key=lambda x: x[1], reverse=True)[:10]

        pg.draw.rect(self.screen, (0, 0, 0), ((0, 0), (self.screen.get_width(), self.screen.get_height())))

        # Title
        title_surface = self.FONT.render("High Scores", True, (255, 255, 255))
        self.place_text(title_surface, 50)

        # Render each entry
        for i, (name, score) in enumerate(sorted_scores):
            color = (255, 255, 255)
            if i == 0:
                color = (255, 215, 0)
            elif i == 1:
                color = (192, 192, 192)
            elif i == 2:
                color = (205, 127, 50)

            text = f"{i + 1}. {name.strip()}: {score}"
            text_surface = self.FONT.render(text, True, color)
            self.place_text(text_surface, 75 + (i + 1) * 25)
        
        continue_surface = self.FONT.render("Press Enter to continue", True, (255, 255, 255))
        self.place_text(continue_surface, 350)

    def event_handler(self, events: List[pg.event.Event]):
        super().event_handler(events)
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.quit()
