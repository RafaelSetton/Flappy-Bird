from time import sleep
from random import randint
from os import listdir
import pygame
pygame.init()
pygame.mixer.init()

IMAGES = {name[:-4]: pygame.image.load(f"Images/{name}") for name in listdir('Images')}


class Bird:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.images = [IMAGES[f'bird{n}'] for n in range(1, 4)]
        self.image: pygame.Surface = self.images[0]
        self.speed = 0
        self.y = 50
        self.alive = True

    @staticmethod
    def rotate_center(image, topleft, angle):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)

        return rotated_image, new_rect.topleft

    def blit(self):
        rotation = min(self.speed*4, 90)
        self.screen.blit(*self.rotate_center(self.image, (100, int(self.y)), -rotation))

    def frame(self):
        self.y = max(self.y + self.speed, 0)
        self.speed += 0.2
        if self.y + self.image.get_height() >= self.screen.get_height():
            self.alive = False


class Pipe:
    def __init__(self, screen: pygame.Surface):
        self.image: pygame.Surface = IMAGES['pipe']
        self.screen = screen
        self.y = randint(150, self.screen.get_height()-150)

    def blit(self, x):
        self.screen.blit(self.image, (x, self.y + 50))
        self.screen.blit(pygame.transform.rotate(self.image, 180), (x, self.y - 50 - self.image.get_height()))


class Game:
    def __init__(self):
        self.dp_height = 500
        self.dp_width = 1000
        self.tela: pygame.Surface = pygame.display.set_mode((self.dp_width, self.dp_height))
        self.pipes = [Pipe(self.tela) for _ in range(5)]
        self.bird = Bird(self.tela)
        self.running = True
        self.points = 0
        self.pipe_x = self.dp_width

    def restart(self):
        image = pygame.transform.scale(IMAGES['Game Over'], (self.tela.get_width(), self.tela.get_height()))
        self.tela.blit(image, (0, 0))
        pygame.display.update()
        while True:
            get = pygame.event.get()
            if [event for event in get if event.type in (pygame.KEYDOWN, pygame.QUIT)]:
                if [event for event in get if event.type == pygame.KEYDOWN]:
                    break
                else:
                    self.running = False
                    break
        self.points = 0
        self.pipe_x = self.dp_width
        self.pipes = [Pipe(self.tela) for _ in range(5)]
        self.bird = Bird(self.tela)

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.bird.speed = -4

    def collision(self):
        center_x = 100 + self.bird.image.get_width()/2
        center_y = self.bird.y + self.bird.image.get_height()/2
        for index in range(len(self.pipes)):
            pipe = self.pipes[index]
            x_ini = self.pipe_x + index*300
            if x_ini <= center_x <= x_ini + pipe.image.get_width() and not pipe.y-50 <= center_y <= pipe.y+50:
                self.bird.alive = False

    def blit(self):
        # BackGround
        x = 0
        image = IMAGES['bg'].convert_alpha()
        while x < self.tela.get_width():
            self.tela.blit(image, (x, 0))
            x += image.get_width()

        # Bird
        self.bird.blit()

        # Pipes
        ind = 0
        while ind < len(self.pipes):
            pipe = self.pipes[ind]
            x = self.pipe_x + ind*300
            if x < -pipe.image.get_width():
                self.pipes.pop(ind)
                self.pipes.append(Pipe(self.tela))
                self.pipe_x += 300
                self.points += 1
                ind -= 1
            else:
                pipe.blit(x)
            ind += 1

        # Points
        points_img = pygame.font.SysFont('Agency FB', 40, True).render(f"{self.points} pts", True, (255, 255, 255))
        pygame.draw.rect(self.tela, (0, 0, 0), ((0, 0), (points_img.get_width() + 20, points_img.get_height() + 20)))
        self.tela.blit(points_img, (10, 10))

    def loop(self):
        while self.running:
            frames = 1
            while self.bird.alive:
                self.blit()

                self.bird.frame()
                self.bird.image = IMAGES[f"bird{1+(frames%30)//10}"]
                self.event_handler()
                self.collision()
                self.pipe_x -= 2

                pygame.display.update()
                frames += 1
                sleep(0.01)

            self.restart()


gm = Game()
gm.loop()
