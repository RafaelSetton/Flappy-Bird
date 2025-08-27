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
        if self.genome.fitness > 1e8 and self.training:
            self.alive = False

    def blit(self):
        # self.draw_network()
        return super().blit()   

    def draw_network(self, pos=(50, 50), size=200):
        """
        Draws a simple visualization of the NEAT network on the given surface.
        pos: top-left position to start drawing
        size: width/height of the network box
        """
        if not hasattr(self, 'genome'):
            return

        # Get nodes and connections
        nodes = list(self.genome.nodes.keys())
        inputs = self.network.input_nodes
        outputs = self.network.output_nodes
        hidden = [k for k in nodes if k not in inputs + outputs]


        # Layout
        layer_y = {
            'input': pos[1] + 20,
            'hidden': pos[1] + size // 2,
            'output': pos[1] + size - 20
        }
        node_pos = {}
        for i, k in enumerate(inputs):
            node_pos[k] = (pos[0] + i * size // (len(inputs)+1), layer_y['input'])
        for i, k in enumerate(hidden):
            node_pos[k] = (pos[0] + i * size // (len(hidden)+1), layer_y['hidden'])
        for i, k in enumerate(outputs):
            node_pos[k] = (pos[0] + i * size // (len(outputs)+1), layer_y['output'])

        # Draw connections
        for cg in self.genome.connections.values():
            if not cg.enabled:
                continue
            start = node_pos.get(cg.key[0])
            end = node_pos.get(cg.key[1])
            if start and end:
                color = (0, 255, 0) if cg.weight > 0 else (255, 0, 0)
                pg.draw.line(self.screen, color, start, end, 2)

        # Draw nodes
        for k, p in node_pos.items():
            pg.draw.circle(self.screen, (200, 200, 200), p, 10)
            pg.draw.circle(self.screen, (0, 0, 0), p, 10, 2)