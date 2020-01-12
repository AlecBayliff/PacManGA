#Alec Bayliff
import numpy as np
from worldgen import World
import copy
class PacMan:
    def __init__(self,world):
        self.world = copy.copy(world)
        self.symbol = 'm'
        self.x_pos = 0
        self.y_pos = 0
        self.score = 0
        
    def move(self):
        roll = np.random.randint(4)
        while(self.valid_roll(roll) == False):
            roll = np.random.randint(4)
        if roll == 0:
            self.x_pos += 1
            if self.world.world[self.x_pos][self.y_pos] == 'p':
                self.score += 1
                self.world.world[self.x_pos][self.y_pos] = ' '
        elif roll == 1:
            self.y_pos += 1
            if self.world.world[self.x_pos][self.y_pos] == 'p':
                self.score += 1
                self.world.world[self.x_pos][self.y_pos] = ' '
        elif roll == 2:
            self.x_pos -= 1
            if self.world.world[self.x_pos][self.y_pos] == 'p':
                self.score += 1
                self.world.world[self.x_pos][self.y_pos] = ' '
        else:
            self.y_pos -= 1
            if self.world.world[self.x_pos][self.y_pos] == 'p':
                self.score += 1
                self.world.world[self.x_pos][self.y_pos] = ' '
                
    def valid_roll(self,roll):
        if roll == 0:
            if self.x_pos == self.world.x_dim-1:
                return False
            elif (self.world.world[self.x_pos+1][self.y_pos] == 'w'):
                return False
        elif roll == 1:
            if self.y_pos == self.world.y_dim-1:
                return False
            elif self.world.world[self.x_pos][self.y_pos+1] == 'w':
                return False
        elif roll == 2:
            if self.x_pos == 0:
                return False
            elif self.world.world[self.x_pos-1][self.y_pos] == 'w':
                return False
        elif roll == 3:
            if self.y_pos == 0:
                return False
            elif self.world.world[self.x_pos][self.y_pos-1] == 'w':
                return False
        return True
        
class Ghost:
    def __init__(self,world,sym):
        self.world = copy.copy(world)
        self.symbol= sym
        self.x_pos = world.x_dim-1
        self.y_pos = world.y_dim-1
        
    def move(self):
        roll = np.random.randint(4)
        while(self.valid_roll(roll) == False):
            roll = np.random.randint(4)
        if roll == 0:
            self.x_pos += 1
        elif roll == 1:
            self.y_pos += 1
        elif roll == 2:
            self.x_pos -= 1
        else:
            self.y_pos -= 1
    def valid_roll(self,roll):
        if roll == 0:
            if self.x_pos == self.world.x_dim-1:
                return False
            elif (self.world.world[self.x_pos+1][self.y_pos] == 'w'):
                return False
        elif roll == 1:
            if self.y_pos == self.world.y_dim-1:
                return False
            elif self.world.world[self.x_pos][self.y_pos+1] == 'w':
                return False
        elif roll == 2:
            if self.x_pos == 0:
                return False
            elif self.world.world[self.x_pos-1][self.y_pos] == 'w':
                return False
        elif roll == 3:
            if self.y_pos == 0:
                return False
            elif self.world.world[self.x_pos][self.y_pos-1] == 'w':
                return False
        return True