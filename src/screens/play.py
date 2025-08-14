from typing import List
from time import sleep
import pygame as pg
import pickle
import json
import neat

from src import IMAGES, NEAT_CONFIG
from src.ai.bird import AIBird
from src.pipe import Pipe
from src.bird import Bird
from .base import BaseScreen


class PlayScreen(BaseScreen):
    def __init__(self, screen, n_players: int, use_ai: bool, **kwargs):
        super().__init__(screen)
        self.points = 0
        self.pipes: List[Pipe] = [Pipe(self.screen, self.screen.get_width() + i * 300) for i in range(5)]
        self.birds: List[Bird] = [Bird(screen, self.pipes[0], i+1) for i in range(n_players)] + self.create_ai_bird(use_ai)
        Pipe.speed = 2

        self.game_over_screen_time = kwargs.get('game_over_screen_time', 1.5)
        self.is_training = kwargs.get('is_training', False)
        
    def create_ai_bird(self, enable: True):
        if not enable:
            return []
        gen = pickle.load(open('data/genomes/goat.pkl', 'rb'))
        netw = neat.nn.FeedForwardNetwork.create(gen, NEAT_CONFIG)
        return [AIBird(self.screen, self.pipes[0], gen, netw, False)]

    @staticmethod
    def check_collision(bird: Bird, pipe: Pipe):
        for x, y in [(bird.x, bird.y),
                    (bird.x + bird.image.get_width(), bird.y),
                    (bird.x, bird.y + bird.image.get_height()),
                    (bird.x + bird.image.get_width(), bird.y + bird.image.get_height())]:
            if pipe.x <= x <= pipe.x + pipe.top_img.get_width() and not pipe.y - 50 <= y <= pipe.y + 50:
                return True

    def handle_collisions(self):
        for bird in self.birds:
            if not bird.alive:
                continue
            for pipe in self.pipes:
                if self.check_collision(bird, pipe):
                    bird.alive = False
                    bird.points = self.points
                    break
        
        # Check if all player birds are dead or AI
        all_players_dead = all(not b.alive for b in self.birds if not isinstance(b, AIBird))
        all_dead = all(not b.alive for b in self.birds)
        if all_dead or (all_players_dead and not self.is_training):
            self.quit()

    def quit(self):
        # Save scores
        json.dump({b.color: b.points for b in self.birds}, open('data/newscores.json', 'w'))
        
        # Show game over screen
        img = pg.transform.scale(IMAGES['Game Over'], (self.screen.get_width(), self.screen.get_height()))
        self.screen.blit(img, (0, 0))
        pg.display.update()
        sleep(self.game_over_screen_time)
        
        return super().quit()

    def blit(self):
        # BackGround
        x = 0
        image = IMAGES['bg'].convert_alpha()
        while x < self.screen.get_width():
            self.screen.blit(image, (x, 0))
            x += image.get_width()

        # Pipes
        ind = 0
        while ind < len(self.pipes):
            pipe = self.pipes[ind]
            if pipe.x + pipe.top_img.get_width() < 0:
                self.pipes.pop(ind)
                self.pipes.append(Pipe(self.screen, pipe.x + 1500))
                self.points += 1
                ind -= 1
            else:
                pipe.blit()
            ind += 1

        # Points
        points_img = self.FONT.render(f"{self.points} pts", True, (255, 255, 255))
        pg.draw.rect(self.screen, (0, 0, 0), ((0, 0), (points_img.get_width() + 20, points_img.get_height() + 20)))
        self.screen.blit(points_img, (10, 10))

    def render(self, frame_n: int, fps: int):
        self.blit()
        self.handle_collisions()

        next_pipe = self.pipes[0] if self.pipes[0].x + self.pipes[0].top_img.get_width() > Bird.x else self.pipes[1]

        for bird in [b for b in self.birds if b.alive]:
            bird.frame()
            if frame_n % (fps // 3) == 0:
                bird.next_image()
            bird.blit()
            bird.next_pipe = next_pipe
        for pipe in self.pipes:
            pipe.move()
        if frame_n % (fps * 40) == 0:  # Every 40 seconds
            Pipe.speed += 1

    def event_handler(self, events: List[pg.event.Event]):
        for event in events:
            if event.type == pg.KEYDOWN:
                for b in self.birds:
                    if b.jump_key == event.unicode and not isinstance(b, AIBird):
                        b.jump()
                        break

