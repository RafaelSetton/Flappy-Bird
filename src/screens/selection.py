from typing import List
import pygame as pg

from .base import BaseScreen
from ..bird import Bird

class SelectionStep:
    CHOOSE_PLAYERS = 0
    AI_SELECTION = 1
    CONFIRMATION = 2
    DONE = 3


class SelectionScreen(BaseScreen):
    def __init__(self, screen):
        super().__init__(screen)
        self.step = SelectionStep.CHOOSE_PLAYERS
        self.num_players = 1
        self.use_ai = False

    def render(self, frame_n: int, fps: int):
        self.screen.fill((0, 0, 0))
        if self.step == SelectionStep.CHOOSE_PLAYERS:
            self.draw_text("Choose number of players (1-3)", 80)
            for i in range(1, 4):
                self.draw_text(f"{i}", 140 + i * 40, selected=(i == self.num_players))
        elif self.step == SelectionStep.AI_SELECTION:
            self.draw_text("Include AI Player?", 120)
            self.draw_text("Yes", 180, selected=self.use_ai)
            self.draw_text("No", 220, selected=not self.use_ai)
        elif self.step == SelectionStep.CONFIRMATION:            
            for i in range(1, self.num_players + 1):
                self.draw_text(f"Player {i}: {Bird.KEYS[i]}", 100 + i * 40, color=Bird.COLORS[i])

            self.draw_text(f"AI: {'Enabled' if self.use_ai else 'Disabled'}", 260)
            self.draw_text("Press Enter to Start", 340)
        pg.display.flip()
    
    def event_handler(self, events: List[pg.event.Event]):
        super().event_handler(events)
        for event in events:
            if event.type == pg.KEYDOWN:
                if self.step == SelectionStep.CHOOSE_PLAYERS:
                    if event.key == pg.K_UP:
                        self.num_players = max(1, self.num_players - 1)
                    elif event.key == pg.K_DOWN:
                        self.num_players = min(3, self.num_players + 1)
                    elif event.key == pg.K_RETURN:
                        self.step = SelectionStep.AI_SELECTION
                elif self.step == SelectionStep.AI_SELECTION:
                    if event.key in [pg.K_UP, pg.K_DOWN]:
                        self.use_ai = not self.use_ai
                    elif event.key == pg.K_RETURN:
                        self.step = SelectionStep.CONFIRMATION
                elif self.step == SelectionStep.CONFIRMATION:
                    if event.key == pg.K_RETURN:
                        self.quit()

