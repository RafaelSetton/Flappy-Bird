import matplotlib.pyplot as plt
from numpy import mean
import neat

from ..game import Game
from .bird import AIBird
from ..screens import PlayScreen


class AITrainer(Game):
    LOGS = []
    
    @staticmethod
    def create_custom_population(config, seed_genome):
        p = neat.Population(config)

        # Create an initial population based on the seed genome
        for i, gid in enumerate(p.population):
            if i == 0:
                # Clone the seed genome into the population
                p.population[gid] = seed_genome
                seed_genome.key = gid
            else:
                # Mutate copies of the seed genome
                g = seed_genome.__class__(gid)
                g.configure_crossover(seed_genome, seed_genome, config.genome_config)
                g.mutate(config.genome_config)
                p.population[gid] = g
        return p

    def loop(self, genomes, config, fps=500):     
        game = PlayScreen(self.tela, 0, False, game_over_screen_time = 0, is_training=True)
        game.birds = list(self.create_birds(genomes, config, game.pipes[0]))
        game.loop(fps)
        self.LOGS.append([bird.genome.fitness for bird in game.birds])

    def create_birds(self, genomes, config, first_pipe):
        for _, genome in genomes:
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            genome.fitness = 0
            yield AIBird(self.tela, first_pipe, genome, net)

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

