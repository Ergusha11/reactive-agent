from agent import *
from item import *

import pygame as pg
import random

n = 26 #rows
m = 42 #columns

pg.font.init() # load fonts

BGPOSITION = (25,25)
BGSIZE = (25*m,25*n)

OBSTACLES = 100

WHITE = (255, 255, 255)
BTTNITEM = pg.image.load('images/buttonItem.png')
BTTNOBS = pg.image.load('images/buttonObs.png')
BTTNITEMSLCT = pg.image.load('images/buttonItemSelect.png')
BTTNOBSSLCT = pg.image.load('images/buttonObsSelect.png')

MYFONT = pg.font.SysFont('Arial', 18) # Configure font

NUM_TUPLE = [2,3,4] # numbers of samples

MAX_NUM = 90 # value max for color

table = [['' for _ in range(m)] for _ in range(n)] # 26 rows x 42 columns


def mainObject() -> None:
    row = random.randint(0, n-1)
    col = random.randint(0, m-1)
    table[row][col] = 'M'
    return (row, col)
    
def obstacle(num: int) -> None:
    for i in range(num):
        row = random.randint(0, n-1)
        col = random.randint(0, m-1)
        if table[row][col] == '':
            table[row][col] = 'O'
        else:
            i -= 1

def items(num: int) -> None:
    for i in range(num):
        row = random.randint(0, n-1)
        col = random.randint(0, m-1)
        if table[row][col] == '':
            item = Item(random.choice(NUM_TUPLE))
            table[row][col] = item
        else:
            i -= 1

def drawObjects(screen: pg.Surface) -> None:
    for i in range(n):
        for j in range(m):
            text_surf = None
            rect = pg.Rect(j*25 + 25, i*25 + 25, 25, 25) 

            if table[i][j] == 'M':
                pg.draw.rect(screen, (255, 0, 0), rect)
                text_surf = MYFONT.render('M', True, (255, 255, 255))
            if table[i][j] == 'O':
                pg.draw.rect(screen, (0, 0, 0), rect)
                text_surf = None
            if isinstance(table[i][j], Item):
                num = table[i][j].getNumItem()
                pg.draw.rect(screen, (0, 255, 0), rect)
                text_surf = MYFONT.render(str(num), True, (255, 255, 255))
            if isinstance(table[i][j], crumbItem):
                num = table[i][j].getNumCrumb()
                intensity = int((num * 4 / MAX_NUM) * 255)
                pg.draw.rect(screen, (intensity, 0, intensity),rect)
                text_surf = MYFONT.render('#', True, (255, 255, 255))

            if text_surf:
                text_rect = text_surf.get_rect(center=rect.center)
                screen.blit(text_surf, text_rect)

def moveAgents(ragents: list, screen: pg.Surface) -> None:
    for ragent in ragents:
        ragent.move()
        if ragent.getHasItem():
            pg.draw.rect(screen, (204, 255, 51), (ragent.col*25 + 25, ragent.row*25 + 25, 25, 25))
        else:
            pg.draw.rect(screen, (30,144,255), (ragent.col*25 + 25, ragent.row*25 + 25, 25, 25))

def showButtons(screen: pg.Surface, bttnItem: bool, bttnObs: bool) -> None:
    if bttnItem:
        screen.blit(BTTNITEMSLCT, (649, 739))
    else:
        screen.blit(BTTNITEM, (649, 739))
        
    if bttnObs:
        screen.blit(BTTNOBSSLCT, (149, 739))
    else: 
        screen.blit(BTTNOBS, (149, 739))


def screenEvents(screen:pg.Surface, event: pg.event, bttnItem: bool, bttnObs: bool) -> tuple[bool, bool]:
    if event.type == pg.MOUSEBUTTONDOWN:
        col , row = event.pos
        if 149 <= col <= 449 and 739 <= row <= 809:
            bttnObs = not bttnObs
            if bttnItem:
                bttnItem = False
        if 649 <= col <= 949 and 739 <= row <= 809:
            bttnItem = not bttnItem
            if bttnObs:
                bttnObs = False

    return bttnItem, bttnObs

def insertElements(bttnItem: bool, bttnObs: bool, event: pg.event):
    if event.type == pg.MOUSEBUTTONDOWN:
        col , row = event.pos
        if  24 < col < 1075 and 24 < row < 675:
            mcol = col // 25
            mrow = row // 25
            print (mrow)
            print (mcol)
            if bttnObs:
                if table[mrow - 1][mcol - 1] == '':
                    table[mrow - 1][mcol - 1] = 'O'
                elif table[mrow - 1][mcol - 1] == 'O':
                    table[mrow - 1][mcol - 1] = ''
            elif bttnItem:
                item = Item(random.choice(NUM_TUPLE))
                if table[mrow - 1][mcol - 1] == '':
                    table[mrow - 1][mcol - 1] = item
                elif isinstance(table[mrow - 1][mcol - 1],Item): 
                    table[mrow - 1][mcol - 1] = ''

def updateScreen(screen: pg.Surface, ragents: list, bttnItem: bool, bttnObs: bool) -> None:
    screen.fill((0,0,0))
    
    pg.draw.rect(screen, (220,220,220), (BGPOSITION, BGSIZE))

    drawObjects(screen)
    moveAgents(ragents, screen)
    showButtons(screen, bttnItem, bttnObs)
