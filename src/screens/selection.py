from typing import List
import pygame as pg

from .base import BaseScreen


class SelectionScreen(BaseScreen):
    # TODO Name Selection and later, Highscores
    def __init__(self, screen):
        super().__init__(screen)
        self.step = 0  # 0 = Choose players, 1 = AI or not, 2 = Done
        self.num_players = 1
        self.use_ai = False

    def draw_text(self, text, y, selected=False, color=None):
        if color is None:
            color = (255, 255, 0) if selected else (255, 255, 255)
        render = self.FONT.render(text, True, color)
        rect = render.get_rect(center=(self.screen.get_width() // 2, y))
        self.screen.blit(render, rect)

    def render(self, frame_n: int, fps: int):
        self.screen.fill((0, 0, 0))
        if self.step == 0:
            self.draw_text("Choose number of players (1-3)", 80)
            for i in range(1, 4):
                self.draw_text(f"{i}", 140 + i * 40, selected=(i == self.num_players))
        elif self.step == 1:
            self.draw_text("Include AI Player?", 120)
            self.draw_text("Yes", 180, selected=self.use_ai)
            self.draw_text("No", 220, selected=not self.use_ai)
        elif self.step == 2:
            self.draw_text(f"Players: {self.num_players}", 140)
            self.draw_text(f"AI: {'Enabled' if self.use_ai else 'Disabled'}", 180)
            self.draw_text("Press Enter to Start", 240)
        pg.display.flip()
    
    def event_handler(self, events: List[pg.event.Event]):
        super().event_handler(events)
        for event in events:
            if event.type == pg.KEYDOWN:
                if self.step == 0:
                    if event.key == pg.K_UP:
                        self.num_players = max(1, self.num_players - 1)
                    elif event.key == pg.K_DOWN:
                        self.num_players = min(3, self.num_players + 1)
                    elif event.key == pg.K_RETURN:
                        self.step = 1
                elif self.step == 1:
                    if event.key in [pg.K_UP, pg.K_DOWN]:
                        self.use_ai = not self.use_ai
                    elif event.key == pg.K_RETURN:
                        self.step = 2
                elif self.step == 2:
                    if event.key == pg.K_RETURN:
                        self.quit()

