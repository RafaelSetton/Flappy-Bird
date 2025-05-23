import pygame as pg
from random import randint

from . import IMAGES


class Pipe:
    speed = 2

    def __init__(self, screen: pg.Surface, x):
        self.bottom_img: pg.Surface = IMAGES['pipe']
        self.top_img: pg.Surface = pg.transform.flip(self.bottom_img, False, True)
        self.screen = screen
        self.y = randint(150, self.screen.get_height()-150)
        self.x = x

    def move(self):
        self.x -= self.speed

    def blit(self):
        self.screen.blit(self.bottom_img, (self.x, self.y + 50))
        self.screen.blit(self.top_img, (self.x, self.y - 50 - self.top_img.get_height()))

