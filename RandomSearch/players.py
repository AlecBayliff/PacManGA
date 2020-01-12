#Alec Bayliff
import numpy as np
import copy
class Player:
    def __init__(self,world,sym):
        self.world = copy.copy(world)
        self._symbol= sym
        self._xpos = world.x_dim()-1
        self._ypos = world.y_dim()-1
        
    def move(self):
        roll = np.random.randint(4)
        while(self.valid_roll(roll) == False):
            roll = np.random.randint(4)
        if roll == 0:
            self._xpos += 1
        elif roll == 1:
            self._ypos += 1
        elif roll == 2:
            self._xpos -= 1
        else:
            self._ypos -= 1
            
    def valid_roll(self,roll):
        if roll == 0:
            if self._xpos == self.world.x_dim()-1:
                return False
            elif (self.world.world_map[self._xpos+1][self._ypos] == 'w'):
                return False
        elif roll == 1:
            if self._ypos == self.world.y_dim()-1:
                return False
            elif self.world.world_map[self._xpos][self._ypos+1] == 'w':
                return False
        elif roll == 2:
            if self._xpos == 0:
                return False
            elif self.world.world_map[self._xpos-1][self._ypos] == 'w':
                return False
        elif roll == 3:
            if self._ypos == 0:
                return False
            elif self.world.world_map[self._xpos][self._ypos-1] == 'w':
                return False
        return True
    
    def x_pos(self):
        return self._xpos
    
    def y_pos(self):
        return self._ypos
    
    def symbol(self):
        return self._symbol
class PacMan(Player):
    def __init__(self,world):
        self.world = copy.copy(world)
        self._symbol = 'm'
        self._xpos = 0
        self._ypos = 0
        self._score = 0
        
    def move(self):
        roll = np.random.randint(4)
        while(self.valid_roll(roll) == False):
            roll = np.random.randint(4)
        if roll == 0:
            self._xpos += 1
            if self.world.world_map[self._xpos][self._ypos] == 'p':
                self._score += 1
                self.world.world_map[self._xpos][self._ypos] = ' '
            elif self.world.world_map[self._xpos][self._ypos] == 'f':
                self._score += 10
                self.world.world_map[self._xpos][self._ypos] = ' '
                self.world.fruit_placed = False
        elif roll == 1:
            self._ypos += 1
            if self.world.world_map[self._xpos][self._ypos] == 'p':
                self._score += 1
                self.world.world_map[self._xpos][self._ypos] = ' '
            elif self.world.world_map[self._xpos][self._ypos] == 'f':
                self._score += 10
                self.world.world_map[self._xpos][self._ypos] = ' '
        elif roll == 2:
            self._xpos -= 1
            if self.world.world_map[self._xpos][self._ypos] == 'p':
                self._score += 1
                self.world.world_map[self._xpos][self._ypos] = ' '
            elif self.world.world_map[self._xpos][self._ypos] == 'f':
                self._score += 10
                self.world.world_map[self._xpos][self._ypos] = ' '
        else:
            self._ypos -= 1
            if self.world.world_map[self._xpos][self._ypos] == 'p':
                self._score += 1
                self.world.world_map[self._xpos][self._ypos] = ' '
            elif self.world.world_map[self._xpos][self._ypos] == 'f':
                self._score += 10
                self.world.world_map[self._xpos][self._ypos] = ' '
    
    def score(self):
        return self._score
        
class Ghost(Player):
    pass