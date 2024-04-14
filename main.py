# Artificial Intelligence Fundamentals. Reactive Agents
# Catonga Tecla Daniel Isaí 
# Hernandez del Angel Erick Gustavo
# 4BV1

from agent import Agent
from drawScreen import obstacle, items, updateScreen, mainObject, screenEvents, insertElements

import pygame as pg
import random
import sys

pg.init()

clock = pg.time.Clock()
screen = pg.display.set_mode((1100, 850)) # 44 colums x 28 rows (each cell is 25x25 pixels)

obstacle(100)
items(10)

def main() -> None:
    rowB, colB = mainObject()
    agents = [Agent((rowB,colB)),Agent((rowB,colB))]
    #agents = [Agent((rowB,colB)),Agent((rowB,colB))]
    bttnItem = False
    bttnObs = False

    while True:
        clock.tick(13)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
                break
                
            
            bttnItem, bttnObs = screenEvents(screen, event, bttnItem, bttnObs)
            insertElements(bttnItem, bttnObs, event)
        
        updateScreen(screen, agents, bttnItem, bttnObs)
        pg.display.flip()



if __name__ == "__main__":
    main()

#pg.quit()
        
