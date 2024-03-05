from agent import Agent
from drawScreen import *

import pygame as pg
import random

pg.init()

clock = pg.time.Clock()
screen = pg.display.set_mode((1100, 700)) # 44 colums x 28 rows (each cell is 25x25 pixels)


def main(ragents: list) -> None:
    running = True

    while running:
        clock.tick(15)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        
        updateScreen(screen, ragents)
        pg.display.flip()


if __name__ == "__main__":
    ragent = Agent()
    ragent2 = Agent()
    main([ragent, ragent2])

pg.quit()
        
