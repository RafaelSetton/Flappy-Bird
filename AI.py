import matplotlib.pyplot as plt
from numpy import mean
from pickle import dump, load
from typing import List
from sys import argv
import neat
from os import path

from main import Game, Bird

LOGS = []


class MyBird(Bird):
    def __init__(self, screen, next_pipe, genome, network, training=True):
        super().__init__(screen, next_pipe)
        self.genome: neat.DefaultGenome = genome
        self.network: neat.nn.FeedForwardNetwork = network
        self.training = training

    def frame(self):
        super().frame()
        net_out = self.network.activate([self.y, self.next_pipe.x, self.next_pipe.y, self.next_pipe.speed])[0]
        if net_out > 0.5:
            self.jump()
        if self.alive:
            self.genome.fitness += 0.01
        if self.genome.fitness > 150 and self.training:
            self.alive = False

    @classmethod
    def eval(cls, genomes, config):
        game = MyGame(genomes, config)
        game.loop(120)


class MyGame(Game):
    def __init__(self, genomes, config):
        super().__init__()
        self.generation = 0
        self.create_birds(genomes, config)

    def create_birds(self, genomes, config):
        self.birds: List[MyBird] = []
        for genome_id, genome in genomes:
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            genome.fitness = 0
            self.birds.append(MyBird(self.tela, self.pipes[0], genome, net))

    def restart(self):
        LOGS.append([bird.genome.fitness for bird in self.birds])
        self.running = False


if __name__ == '__main__':
    mode = argv[1]
    config_file = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                              neat.DefaultSpeciesSet, neat.DefaultStagnation,
                              path.join(path.dirname(__file__), "NEAT_config.txt"))
    if mode == 'train':
        # Train AI
        p = neat.Population(config_file)
        winner = p.run(MyBird.eval, 10)
        dump(winner, open('genome.pickle', 'wb'))

        print("\nBest Genome:", winner, sep='\n')

        # Plot Graph
        means = [mean(log) for log in LOGS]
        plt.plot(range(len(means)), means)
        for index, gen in enumerate(LOGS):
            plt.scatter([index] * len(gen), gen)

        plt.title("Resultados")
        plt.ylabel("Seconds Survived")
        plt.xlabel("Generation")
        plt.xticks(range(0, len(LOGS)+1, 1))
        plt.show()
    elif mode == 'play':
        # Play with AI
        gen = load(open('genome.pickle', 'rb'))
        netw = neat.nn.FeedForwardNetwork.create(gen, config_file)
        gm = MyGame([], None)
        gm.birds = [MyBird(gm.tela, gm.pipes[0], gen, netw, False)]
        gm.loop(80)
    else:
        print("python AI.py train: Train the AI\n"
              "python AI.py play: Watch the saved AI play")
