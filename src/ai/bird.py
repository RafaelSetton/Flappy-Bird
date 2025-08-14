import neat
import pygame as pg

from src.pipe import Pipe
from ..bird import Bird

class AIBird(Bird):
    def __init__(self, screen: pg.Surface, next_pipe: Pipe, genome: neat.DefaultGenome, network: neat.nn.FeedForwardNetwork, training: bool = True):
        super().__init__(screen, next_pipe)
        self.genome = genome
        self.network = network
        self.training = training
        self.skip_frames = 120

    @property
    def is_ai(self) -> bool:
        return True

    def frame(self):
        super().frame()
        net_out = self.network.activate([self.y, self.next_pipe.x, self.next_pipe.y, self.next_pipe.speed, self.speed])[0]
        if net_out > 0.5:
            self.jump()
            self.genome.fitness -= .07
        if self.skip_frames > 0:
            self.skip_frames -= 1
        elif self.alive:
            self.genome.fitness += .1
        if self.genome.fitness > 1500 and self.training:
            self.alive = False
