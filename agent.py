from drawScreen import *
import pygame as pg
import random

class Agent():
    # Constructor
    def __init__(self, mainObjects_: tuple):
        self.col = random.randint(0, m - 1)
        self.row = random.randint(0, n - 1)
        self.mainObjects = mainObjects_
        
        self.base_row = mainObjects_[0]
        self.base_col = mainObjects_[1]

        self.hasItem = False

    # Getters and setters
    def getPosition(self) -> tuple:
        return (self.col, self.row)
    
    def setPosition(self, col: int, row: int) -> None:
        self.col = col
        self.row = row

    def getHasItem(self) -> bool:
        return self.hasItem
    
    def invertHasItem(self) -> None:
        self.hasItem = not self.hasItem

    # Sensors for the agent
    def northSensor(self) -> bool:
        return self.row > 0 and table[self.row - 1][self.col] != 'O'
    
    def southSensor(self) -> bool:
        return self.row < n - 1 and table[self.row + 1][self.col] != 'O'
    
    def eastSensor(self) -> bool:
        return self.col < m - 1 and table[self.row][self.col + 1] != 'O'
    
    def westSensor(self) -> bool:
        return self.col > 0 and table[self.row][self.col - 1] != 'O'

    # Agent's behavior
    def randomStep(self) -> tuple:
        possibleSteps = []
        if self.northSensor():
            possibleSteps.append((-1, 0))
        if self.southSensor():
            possibleSteps.append((1, 0))
        if self.eastSensor():
            possibleSteps.append((0, 1))
        if self.westSensor():
            possibleSteps.append((0, -1))

        return random.choice(possibleSteps)

    def movetoBase(self) -> None:
        possible_moves = []

        if self.col < self.base_col:
            if self.eastSensor():
                print("R sensor")
                possible_moves.append((0,1))
        elif self.col > self.base_col:
            if self.westSensor():
                possible_moves.append((0,-1))
                print("L sensor")

        if self.row < self.base_row:
            if self.southSensor():
                possible_moves.append((1,0))
        elif self.row > self.base_row:
            if self.northSensor():
                possible_moves.append((-1,0))
        
        if len(possible_moves) == 0:
            row , column = self.randomStep()
        else:
            row , column = random.choice(possible_moves)    

        
        self.setPosition(self.col + column, self.row + row)
    
    def move(self) -> None:
        if self.getHasItem():
            if table[self.row][self.col] == 'M':
                self.invertHasItem()
                return
                
            print("I have an item")
            self.movetoBase()
        else:
            row,column = self.randomStep()
            if table[self.row + row][self.col + column] == 'I':
                self.invertHasItem()
                table[self.row + row][self.col + column] = ''   
            self.setPosition(self.col + column, self.row + row)
    