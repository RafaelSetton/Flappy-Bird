import pygame as pg

from . import BIRD_IMAGES
from .pipe import Pipe

class Bird:
    x = 100
    G = 0.2

    COLORS = ["base", "red", "green", "blue"]
    KEYS = ' qpb'

    def __init__(self, screen: pg.Surface, next_pipe: Pipe, id: int = 0):
        self.jump_key = self.KEYS[id]
        self.screen = screen
        self.color = self.COLORS[id]
        self.images = BIRD_IMAGES[self.color]
        self.image_n = 0
        self.speed = 0
        self.y = 50
        self.alive = True
        self.next_pipe = next_pipe
        self.points = 0

    @property
    def is_ai(self) -> bool:
        return False

    @property
    def image(self) -> pg.Surface:
        return self.images[self.image_n]

    def next_image(self):
        self.image_n = (self.image_n + 1) % 3

    @staticmethod
    def rotate_center(image, topleft, angle):
        rotated_image = pg.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)

        return rotated_image, new_rect.topleft

    def blit(self):
        rotation = min(self.speed * 4, 90)
        self.screen.blit(*self.rotate_center(self.image, (self.x, int(self.y)), -rotation))

    def frame(self):
        self.y = max(self.y + self.speed, 0)
        self.speed += self.G
        if self.y + self.image.get_height() >= self.screen.get_height():
            self.alive = False

    def jump(self):
        self.speed = -4.5

