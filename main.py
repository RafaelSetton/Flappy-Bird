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
        # Train AI
        p = neat.Population(NEAT_CONFIG)
        trainer = AITrainer()
        winner = p.run(trainer.loop, 10)
        pg.quit()

        AITrainer.plot()

        name = input("Name for this genome: ")
        if name.strip():
            pickle.dump(winner, open(f"data/genomes/{name.strip()}.pickle", 'wb'))

        print("\nBest Genome:", winner, sep='\n')
