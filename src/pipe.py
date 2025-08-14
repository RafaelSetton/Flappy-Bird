import pygame as pg
from random import randint

from . import IMAGES


class Pipe:
    speed = 2
    bottom_img: pg.Surface = IMAGES['pipe']
    top_img: pg.Surface = pg.transform.flip(bottom_img, False, True)

    def __init__(self, screen: pg.Surface, x):
        self.screen = screen
        self.y = randint(150, self.screen.get_height()-150)
        self.x = x

    def move(self):
        self.x -= self.speed

    def blit(self):
        self.screen.blit(self.bottom_img, (self.x, self.y + 50))
        self.screen.blit(self.top_img, (self.x, self.y - 50 - self.top_img.get_height()))

