from random import randint
from os import listdir
from typing import List
import pygame as pg
pg.init()
pg.mixer.init()

IMAGES = {name[:-4]: pg.image.load(f"Images/{name}") for name in listdir('Images')}


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


class Bird:
    x = 100

    def __init__(self, screen: pg.Surface, next_pipe: Pipe):
        self.screen = screen
        self.images = [IMAGES[f'bird{n}'] for n in range(1, 4)]
        self.image: pg.Surface = self.images[0]
        self.speed = 0
        self.y = 50
        self.alive = True
        self.next_pipe = next_pipe

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
        self.speed += 0.2
        if self.y + self.image.get_height() >= self.screen.get_height():
            self.alive = False

    def jump(self):
        self.speed = -5


class Game:
    def __init__(self):
        self.dp_height = 500
        self.dp_width = 1000
        self.tela: pg.Surface = pg.display.set_mode((self.dp_width, self.dp_height))
        self.running = True
        self.points = 0
        self.pipes: List[Pipe] = []
        self.birds: List[Bird] = []
        self.create_items()
        Pipe.speed = 2

    def create_items(self):
        self.pipes = [Pipe(self.tela, self.dp_width + i * 300) for i in range(5)]
        self.birds = [Bird(self.tela, self.pipes[0])]

    def restart(self):
        image = pg.transform.scale(IMAGES['Game Over'], (self.tela.get_width(), self.tela.get_height()))
        self.tela.blit(image, (0, 0))
        pg.display.update()
        loop = True
        while loop:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    loop = False
                elif event.type == pg.QUIT:
                    self.running = False
                    loop = False
        self.points = 0
        self.create_items()

    def event_handler(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.birds = []
                self.running = False
            elif event.type == pg.KEYDOWN:
                self.birds[0].jump()

    def collision(self):
        for bird in self.birds:
            for pipe in self.pipes:
                for x, y in [(bird.x, bird.y),
                             (bird.x + bird.image.get_width(), bird.y),
                             (bird.x, bird.y + bird.image.get_height()),
                             (bird.x + bird.image.get_width(), bird.y + bird.image.get_height())]:
                    if pipe.x <= x <= pipe.x + pipe.top_img.get_width() and not pipe.y - 50 <= y <= pipe.y + 50:
                        bird.alive = False
                        break
                else:
                    continue
                break

    def blit(self):
        # BackGround
        x = 0
        image = IMAGES['bg'].convert_alpha()
        while x < self.tela.get_width():
            self.tela.blit(image, (x, 0))
            x += image.get_width()

        # Pipes
        ind = 0
        while ind < len(self.pipes):
            pipe = self.pipes[ind]
            if pipe.x + pipe.top_img.get_width() < 0:
                self.pipes.pop(ind)
                self.pipes.append(Pipe(self.tela, pipe.x + 1500))
                self.points += 1
                ind -= 1
            else:
                pipe.blit()
            ind += 1

        # Points
        points_img = pg.font.SysFont('Agency FB', 40, True).render(f"{self.points} pts", True, (255, 255, 255))
        pg.draw.rect(self.tela, (0, 0, 0), ((0, 0), (points_img.get_width() + 20, points_img.get_height() + 20)))
        self.tela.blit(points_img, (10, 10))

    def loop(self, fps=80):
        clock = pg.time.Clock()
        while self.running:
            frames = 1
            while any([bird.alive for bird in self.birds]):
                self.blit()
                self.event_handler()
                self.collision()

                next_pipe = self.pipes[0] if self.pipes[0].x + self.pipes[0].top_img.get_width() > Bird.x \
                    else self.pipes[1]

                for bird in [b for b in self.birds if b.alive]:
                    bird.frame()
                    bird.image = IMAGES[f"bird{1+(frames%30)//10}"]
                    bird.blit()
                    bird.next_pipe = next_pipe
                for pipe in self.pipes:
                    pipe.move()
                if frames % (fps * 40) == 0:  # Every 40 seconds
                    Pipe.speed += 1

                pg.display.update()
                frames += 1
                clock.tick(fps)

            if self.running:
                self.restart()


if __name__ == '__main__':
    Game().loop()
