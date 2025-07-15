#Alec Bayliff
import numpy as np
import copy
import controller

class Player:            
    def valid_roll(self,even,pos):
        if even ==True and pos == True:
            if self._xpos == self.world.x_dim()-1:
                return False
            elif (self.world.world_map()[self._xpos+1][self._ypos] == 'w'):
                return False
        elif even == True and pos == False:
            if self._ypos == self.world.y_dim()-1:
                return False
            elif self.world.world_map()[self._xpos][self._ypos+1] == 'w':
                return False
        elif even == False and pos== True:
            if self._xpos == 0:
                return False
            elif self.world.world_map()[self._xpos-1][self._ypos] == 'w':
                return False
        elif even == False and pos == False:
            if self._ypos == 0:
                return False
            elif self.world.world_map()[self._xpos][self._ypos-1] == 'w':
                return False
        return True
    
    def x_pos(self):
        return self._xpos
    
    def y_pos(self):
        return self._ypos
    
    def symbol(self):
        return self._symbol
    
    def controller(self):
        return self._controller
    
    def set_controller(self):
        self._controller = controller
        
    def score(self):
        return self._score
        
    def set_score(self,score):
        self._score = score
        
    def update_score(self,score):
        self._score = self._score + score
        
    def final_score(self):
        self._score = self._score / self._controller.size()
    
class PacMan(Player):
    def __init__(self,mdepth,size,prob,world):
        self.world = copy.copy(world)
        self._symbol = 'm'
        self._xpos = 0
        self._ypos = 0
        self._score = 0
        self._controller = controller.PacController(mdepth,size,prob)
        
    def move(self,inval):
        if inval != np.inf and inval != -np.inf:
            if inval % 2 == 0:
                even = True
            else:
                even = False
        else:
            rnum = np.random.rand()
            if rnum >= .5:
                even = True
            else:
                even = False
        if inval >= 0:
            pos = True
        else:
            pos = False

        while(self.valid_roll(even,pos) == False):
            roll = np.random.randint(4)
            match roll:
                case 0:
                    even = True
                case 1:
                    even = False
                case 2:
                    pos = True
                case 3:
                    pos = False
        if even == True and pos == True:
            self._xpos += 1
            self.check_coords()
        elif even == True and pos == False:
            self._ypos += 1
            self.check_coords()
        elif even == False and pos == True:
            self._xpos -= 1
            self.check_coords()
        else:
            self._ypos -= 1
            self.check_coords()
                
    def check_coords(self):
        if self.world.world_map()[self._xpos][self._ypos] == 'p':
            self.world.remove_pill(self._xpos,self._ypos)
            self._score += 1
            self.world.world_map()[self._xpos][self._ypos] = ' '
        elif self.world.world_map()[self._xpos][self._ypos] == 'f':
            self._score += 10
            self.world.world_map()[self._xpos][self._ypos] = ' '
            self.world.remove_fruit()
    
    def win_score(self,t,tmult):
        #PacMan win score = (total score * 2-(time/total time)) / parsimony pressure (ln controller size)
        self._score = self._score * (2-(t/tmult))
        self._score = self.score / np.log(self._controller.size())
        
class Ghost(Player):
    def __init__(self,mdepth,size,prob,world,sym):
        self.world = copy.copy(world)
        self._symbol= sym
        self._xpos = world.x_dim()-1
        self._ypos = world.y_dim()-1
        self._score = 0
        self._controller = controller.GhostController(mdepth,size,prob,sym)
        
    def move(self,inval):
        if inval != np.inf and inval != -np.inf:
            if inval % 2 == 0:
                even = True
            else:
                even = False
        else:
            rnum = np.random.rand()
            if rnum >= .5:
                even = True
            else:
                even = False
        if inval >= 0:
            pos = True
        else:
            pos = False
        while(self.valid_roll(even,pos) == False):
            roll = np.random.randint(4)
            match roll:
                case 0:
                    even = True
                    pos = True
                case 1:
                    even = True
                    pos = False
                case 2:
                    even = False
                    pos = True
                case 3:
                    even = False
                    pos = False
        if even == True and pos == True:
            self._xpos += 1
        elif even == True and pos == False:
            self._ypos += 1
        elif even == False and pos == True:
            self._xpos -= 1
        else:
            self._ypos -= 1