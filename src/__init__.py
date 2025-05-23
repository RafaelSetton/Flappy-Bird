import pygame as pg
from os import listdir, path
import neat

IMAGES = {name[:-4]: pg.image.load(f"src/assets/{name}") for name in listdir('src/assets') if name.endswith('.png')}
BIRD_IMAGES = {color: [pg.image.load(f"src/assets/birds/{color}/{i}.png") for i in range(1, 4)] for color in listdir('src/assets/birds')}
NEAT_CONFIG = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                              neat.DefaultSpeciesSet, neat.DefaultStagnation,
                              path.join(path.dirname(__file__), "../NEAT_config.txt"))