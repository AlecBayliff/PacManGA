#Alec Bayliff
import numpy as np
import controller

class Player:            
    @property
    def x_pos(self):
        return self._xpos
    
    @property
    def y_pos(self):
        return self._ypos
    
    @property
    def symbol(self):
        return self._symbol
    
    @symbol.setter
    def symbol(self,sym):
        self._symbol = sym
    
    @property
    def controller(self):
        return self._controller
    
    @controller.setter
    def controller(self):
        self._controller = controller
        
    @property
    def score(self):
        return self._score
    
    @score.setter
    def score(self,score):
        self._score = score
        
    @property
    def allscores(self):
        return self._allscores
    
    @allscores.setter
    def allscores(self,val):
        self._allscores = val
        
    @property
    def identifier(self):
        return self._id
    
    @identifier.setter
    def identifier(self,val):
        self._id = val
        
    def valid_roll(self,even,pos):
        if even ==True and pos == True:
            if self._xpos == self._world.x_dim-1:
                return False
            elif (self._world.world_map[self._xpos+1][self._ypos] == 'w'):
                return False
        elif even == True and pos == False:
            if self._ypos == self._world.y_dim-1:
                return False
            elif self._world.world_map[self._xpos][self._ypos+1] == 'w':
                return False
        elif even == False and pos== True:
            if self._xpos == 0:
                return False
            elif self._world.world_map[self._xpos-1][self._ypos] == 'w':
                return False
        elif even == False and pos == False:
            if self._ypos == 0:
                return False
            elif self._world.world_map[self._xpos][self._ypos-1] == 'w':
                return False
        return True
        
    def update_score(self,score):
        self._score = self._score + score
        
    def final_score(self):
        self._score = self._score / np.log10(self._controller.size())
        
    def load_world(self,world):
        self._world = world
        
    def update_allscores(self,score):
        if isinstance(score,list):
            self._allscores.extend(score)
        else:
            self._allscores.append(score)
        
    def reset_scores(self):
        self._allscores = []
    
class PacMan(Player):
    def __init__(self,idno,mdepth,size,prob):
        self._id = idno
        self._symbol = 'm'
        self._xpos = 0
        self._ypos = 0
        self._score = 0
        self._controller = controller.PacController(mdepth,size,prob)
        self._allscores = []
        
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
        if self._world.world_map[self._xpos][self._ypos] == 'p':
            self._score += 1
            self._world.world_map[self._xpos][self._ypos] = ' '
            self._world.remove_pill(self._xpos,self._ypos)
        elif self._world.world_map[self._xpos][self._ypos] == 'f':
            self._score += 10
            self._world.world_map[self._xpos][self._ypos] = ' '
            self._world.remove_fruit()
    
    def win_score(self,t,tmult):
        #PacMan win score = (total score * 2-(time/total time)) / parsimony pressure (ln controller size)
        self._score = self._score * (2-(t/tmult))
        self._score = self._score / np.log10(self._controller.size())
        
    def reset(self):
        self._xpos = 0
        self._ypos = 0
        self._score = 0
        
class Ghost(Player):
    def __init__(self,idno,mdepth,size,prob,sym,xdim,ydim):
        self._id = idno
        self._symbol = sym
        self._xpos = xdim-1
        self._ypos = ydim-1
        self._score = 0
        self._controller = controller.GhostController(mdepth,size,prob,sym)
        self._allscores = []
        
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
        
    def reset(self,xdim,ydim):
        self._score = 0
        self._xpos = xdim - 1
        self._ypos = ydim - 1