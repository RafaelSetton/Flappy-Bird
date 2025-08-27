import pygame as pg
import neat
import pickle
from argparse import ArgumentParser

from src import NEAT_CONFIG
from src.ai.trainer import AITrainer
from src.game import Game

if __name__ == '__main__':
    parser = ArgumentParser("Flappy Bird")
    parser.add_argument(
        "mode",
        choices=["train", "play"],
        help="Mode to run: 'train' to train AI or 'play' to play the game"
    )
    
    args = parser.parse_args()

    pg.init()
    pg.mixer.init()
    if args.mode == 'play':
        Game().loop()
    else:
        load_from = input("Select a model to train (blank to start from scratch): ")
        if load_from:
            with open(f"data/genomes/{load_from}.pkl", 'rb') as f:
                p = AITrainer.create_custom_population(NEAT_CONFIG, pickle.load(f))
        else:
            p = neat.Population(NEAT_CONFIG)
        
        # Train AI
        trainer = AITrainer()
        winner = p.run(trainer.loop, 40)
        pg.quit()

        AITrainer.plot()

        name = input("Name for this genome (Blank to skip): ")
        if name.strip():
            pickle.dump(winner, open(f"data/genomes/{name.strip()}.pkl", 'wb'))

        print("\nBest Genome:", winner, sep='\n')
