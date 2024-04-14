from drawScreen import table, m, n
from item import *
import heapq
import pygame as pg
import random
import math

class Agent():
    # Constructor
    def __init__(self, mainObjects_: tuple):
        self.col = random.randint(0, m - 1)
        self.row = random.randint(0, n - 1)
        self.mainObjects = mainObjects_
        
        self.base_row = mainObjects_[0]
        self.base_col = mainObjects_[1]

        self.hasItem = False
        self.route = []

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
    def northSensor(self, row:int, col:int) -> bool:
        return row > 0 and table[row - 1][col] != 'O'
    
    def southSensor(self,row:int,col:int) -> bool:
        return row < n - 1 and table[row + 1][col] != 'O'
    
    def eastSensor(self,row:int,col:int) -> bool:
        return col < m - 1 and table[row][col + 1] != 'O'
    
    def westSensor(self,row:int,col:int) -> bool:
        return col > 0 and table[row][col - 1] != 'O'
    
    def crumbSensor(self,row:int,col:int) -> tuple:
        numCrumb = []
        directions = [
            (-1, 0), (1, 0), (0, 1), (0, -1)
        ]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if new_row > 0 and new_row < n-1 and new_col < m-1 and new_col > 0: 
                current_cell = table[new_row][new_col]
                if isinstance(current_cell, crumbItem):
                    numCrumb.append((new_row, new_col, current_cell.getNumCrumb(), False))
                elif isinstance(current_cell, Item):
                    numCrumb.append((new_row, new_col, 0, True))
        return numCrumb

    #Agent's behavior
    def randomStep(self,row:int,col:int) -> tuple:
        possibleSteps = []
        if self.northSensor(row,col):
            possibleSteps.append((-1, 0))
        if self.southSensor(row,col):
            possibleSteps.append((1, 0))
        if self.eastSensor(row,col):
            possibleSteps.append((0, 1))
        if self.westSensor(row,col):
            possibleSteps.append((0, -1))
            
        if len(possibleSteps) > 0:
            return random.choice(possibleSteps)
        return (0,0)

   # def movetoBase(self) -> None:
   #     possible_moves = []

   #     if self.col < self.base_col:
   #         if self.eastSensor():
   #             possible_moves.append((0,1))
   #     elif self.col > self.base_col:
   #         if self.westSensor():
   #             possible_moves.append((0,-1))

   #     if self.row < self.base_row:
   #         if self.southSensor():
   #             possible_moves.append((1,0))
   #     elif self.row > self.base_row:
   #         if self.northSensor():
   #             possible_moves.append((-1,0))
   #     
   #     if len(possible_moves) == 0:
   #         row , column = self.randomStep()
   #     else:
   #         row , column = random.choice(possible_moves)    

   #     
   #     self.setPosition(self.col + column, self.row + row)
    
    def neighbor(self, row:int, col:int) -> list:
        possibleSteps = []
        if self.northSensor(row,col):
            if table[row -1][col] == 'O':
                print("Hay un ostaculo norte")
            possibleSteps.append((row - 1,col))
            #possibleSteps.append((-1, 0))
        if self.southSensor(row,col):
            if table[row + 1][col] == 'O':
                print("Hay un ostaculo sur")
            possibleSteps.append((row + 1,col))
            #possibleSteps.append((1, 0))
        if self.eastSensor(row,col):
            if table[row][col+1] == 'O':
                print("Hay un ostaculo este")
            possibleSteps.append((row,col+1))
            #possibleSteps.append((0, 1))
        if self.westSensor(row,col):
            if table[row][col - 1] == 'O':
                print("Hay un ostaculo oeste")
            possibleSteps.append((row,col - 1))
            #possibleSteps.append((0, -1))
        return possibleSteps    
        #if len(possibleSteps) > 0:
        #    return possibleSteps
        #return (0,0)

    def distanceManhattan(self, x: tuple,y: tuple) -> int:
        return abs(x[0] - y[0]) + abs(x[1] - y[1])
    
    def distanceEuclidean(self, start, end):
        (x1, y1) = start
        (x2, y2) = end
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def A_Star(self) -> tuple:
        # position[0]=col and position[1]=row
        col , row = self.getPosition()
        position = (row,col)
        #print(position)
        openSet = []
        closedSet = set()
        path = {}
        gFuntion = {}
        fFuntion = {}

        gFuntion[position] = 0
        fFuntion[position] = self.distanceManhattan(position,(self.base_col,self.base_row))
        heapq.heappush(openSet,(fFuntion[position],position))
        while openSet:
            #print(openSet)
            #print("Se esta calculando")
            valueF, position = heapq.heappop(openSet)
            #print("Es la posicion", position)
            closedSet.add(position)

            if table[position[0]][position[1]] == 'M':
                route = []
                while position in path:
                    route.append(position)
                    position = path[position]
                route.append((self.row,self.col))
                return route

            for neighbor in self.neighbor(position[0],position[1]):
                #print("Se calculo los vecinos")
                #print(neighbor)
                gNeighbor = gFuntion[position] + 1
                if neighbor not in gFuntion or gNeighbor < gFuntion[neighbor]:
                    path[neighbor] = position
                    gFuntion[neighbor] = gNeighbor
                    fFuntion[neighbor] = gNeighbor + self.distanceManhattan(neighbor,(self.base_col,self.base_row))
                    if not(neighbor in closedSet):
                        heapq.heappush(openSet,(fFuntion[neighbor],neighbor))
        return {}

    def migajaItem(self) -> bool:
        #print("Entre a la funcion")
        if self.getHasItem():
            if table[self.row][self.col] == '':
                crumb = crumbItem(2) 
                table[self.row][self.col] = crumb

            elif isinstance(table[self.row][self.col],crumbItem):
                refCrumb = table[self.row][self.col]
                num = refCrumb.getNumCrumb()
                num += 2
                refCrumb.setNumCrumb(num)
            return True
        else:
            if isinstance(table[self.row][self.col],crumbItem) or table[self.row][self.col] == 'M':
                refCrumb = table[self.row][self.col]
                if refCrumb != 'M':
                    num = refCrumb.getNumCrumb() - 1
                    refCrumb.setNumCrumb(num)
                if refCrumb != 'M' and num == 0 :
                    table[self.row][self.col] = ''
                
                numCrumb = self.crumbSensor(self.row,self.col) 
                #print("posicion actual:",self.getPosition())
                if numCrumb:
                    distance = []
                    for crumb in numCrumb:
                        row, col, count, has_item = crumb
                        item_priority = 5 if has_item else 0  # Prioriza casillas con ítems si son detectados
                        dist = -self.distanceEuclidean((row, col), (self.base_col, self.base_row)) - (count * 1.8) - item_priority
                        heapq.heappush(distance, (dist, row, col))
                        #print(distance)

                    _, row, col = heapq.heappop(distance)  # Ahora esta extrae la mayor distancia
                    self.setPosition(col, row)
                    
                    return True
                else:
                    row,column = self.randomStep(self.row,self.col)
                    self.setPosition(self.col + column, self.row + row)
                    return True

        return False
        

    def move(self) -> None:
        if self.getHasItem():
            if table[self.row][self.col] == 'M':
                print("Item has been delivered")
                self.invertHasItem()
                self.migajaItem()
                self.route = []
                return
                
            #self.movetoBase()
            row,column = self.route.pop()
            print(self.route)
            self.setPosition(column,row)

            # create crumbItem
            self.migajaItem()
            
        else:
            if isinstance(table[self.row][self.col],Item):
                ref_item = table[self.row][self.col]
                num_item = ref_item.getNumItem()
                num_item -= 1
                ref_item.setNumItem(num_item)
                print("Item has been collected")
                self.invertHasItem()
                
                self.route = self.A_Star()
                print(self.route)
                if not self.route:
                    self.route = self.A_Star()
                if num_item == 0:
                    table[self.row][self.col] = ''


        # Case crumb
        column ,row = self.getPosition()
        row,column = self.randomStep(row,column)
        if not self.migajaItem():
            self.setPosition(self.col + column, self.row + row)
