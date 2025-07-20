from typing import List
import pygame as pg
pg.font.init()


class BaseScreen:
    FONT = pg.font.SysFont("Arial", 30)

    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.running = True

    def render(self, frame_n: int, fps: int):
        raise NotImplementedError()
    
    def event_handler(self, events: List[pg.event.Event]):
        for evt in events:
            if evt.type == pg.QUIT:
                exit(1)
    
    def draw_text(self, text, y, selected=False, color=None):
        if color is None:
            color = (255, 255, 0) if selected else (255, 255, 255)
        render = self.FONT.render(text, True, color)
        rect = render.get_rect(center=(self.screen.get_width() // 2, y))
        self.screen.blit(render, rect)

    def quit(self):
        self.running = False
    
    def loop(self, fps=60):
        clock = pg.time.Clock()
        frame_count = 0
        while self.running:
            self.render(frame_count, fps)
            frame_count += 1
            pg.display.update()
            self.event_handler(pg.event.get())
            clock.tick(fps)

