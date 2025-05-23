import matplotlib.pyplot as plt
from numpy import mean
import neat

from ..game import Game
from .bird import AIBird
from ..screens import PlayScreen


class AITrainer(Game):
    LOGS = []
    
    def loop(self, genomes, config, fps=200):     
        game = PlayScreen(self.tela, 0, False, game_over_screen_time = 0)
        game.birds = list(self.create_birds(genomes, config, game.pipes[0]))
        game.loop(fps)
        self.LOGS.append([bird.genome.fitness for bird in game.birds])

    def create_birds(self, genomes, config, first_pipe):
        for genome_id, genome in genomes:
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            genome.fitness = 0
            yield AIBird(self.tela, first_pipe, genome, net)

    @classmethod
    def train(cls, genomes, config):
        game = cls()
        birds = game.loop(genomes, config)
        cls.LOGS.append([bird.genome.fitness for bird in birds])

    @classmethod
    def plot(cls):
        # Plot Graph
        means = [mean(log) for log in cls.LOGS]
        plt.plot(range(len(means)), means)
        for index, gen in enumerate(cls.LOGS):
            plt.scatter([index] * len(gen), gen)

        plt.title("Resultados")
        plt.ylabel("Seconds Survived")
        plt.xlabel("Generation")
        plt.xticks(range(0, len(cls.LOGS)+1, 1))
        plt.show()

