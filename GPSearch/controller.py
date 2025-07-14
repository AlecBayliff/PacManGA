# -*- coding: utf-8 -*-
"""
Created on Tue Jul  8 18:30:30 2025

@author: Alec
"""
import numpy as np
from tree import PacTree,GhostTree
import scipy as sp
from scipy.spatial.distance import cityblock


class Controller:
    def evaluate(self,pac,ghost,world):
        controller = self.get_controller()
        output = self.operate(controller,pac,ghost,world)
        output = np.rint(output)
        return output
    
    def operate(self,node,m,g,world):
        children = node.get_children()
        inputs = []
        if children:
            for child in children:
                inputs.append(self.operate(child,m,g,world))
            match node.get_operator():
                case '+':
                    return np.sum(inputs)
                case '-':
                    a = inputs[0]
                    for b in inputs[1:]:
                        a = a - b
                    return a
                case '*':
                    return np.prod(inputs)
                case '/':
                    a = inputs[0]
                    for b in inputs[1:]:
                        if b != 0:
                            a = a / b
                        else:
                            #Return a number higher than the maximum distance of the worold
                            return np.sqrt(np.square(world.x_dim())+np.square(world.y_dim()))+1
                    return a
                case 'r':
                    rnum = np.random.randint(0,len(inputs))
                    return inputs[rnum]
        else:
            return self.check_operator(node,m,g,world)
        
    def get_controller(self):
        return self._controller

    def manhattan_pill(self,m,world):
        coords = []
        for w in range(world.x_dim()):
            for z in range(world.y_dim()):
                if world.world_map()[w][z] == 'p':
                    coords.append([w,z])
        return sp.spatial.distance.cdist([[m.x_pos(),m.y_pos()]],coords,'cityblock').min()
    
    def manhattan_fruit(self,player,world):
        if world.fruit():
            coords = world.fruit()
            return cityblock([player.x_pos(),player.y_pos()],coords)

        else:
            return world.x_dim() * world.y_dim()

    def walls(self,m,world):
        return world.count_walls(m.x_pos(),m.y_pos())
    
    def size(self):
        return self._size
    
class PacController(Controller):
    def __init__(self,mdepth,size,prob):
        self._tree = PacTree(mdepth,size,prob)
        self._controller = self._tree.get_root()
        self._size = self._tree.get_terminals()[-1]
                
    def manhattan_ghost(self,m,g):
        distances = []
        for ghost in g:
            distances.append(cityblock([m.x_pos(),m.y_pos()],[ghost.x_pos(),ghost.y_pos()]))
        return np.min(distances)
    
    def check_operator(self,node,m,g,world):
        match node.get_operator():
            case 'ghost':
                return self.manhattan_ghost(m,g)
            case 'pill':
                return self.manhattan_pill(m,world)
            case 'walls':
                return self.walls(m,world)
            case 'fruit':
                return self.manhattan_fruit(m,world)
            case 'rand':
                return np.random.normal(0,np.sqrt(np.square(world.x_dim())+np.square(world.y_dim()))+1)
                
class GhostController(Controller):
    def __init__(self,mdepth,size,prob,ego):
        self._tree = GhostTree(mdepth,size,prob)
        self._controller = self._tree.get_root()
        self._size = self._tree.get_terminals()[-1]
        self._ego = ego
                
    def manhattan_pac(self,m,g):
        for ghost in range(len(g)):
            if g[ghost].symbol() == self._ego:
                ego = g[ghost]
        return cityblock([m.x_pos(),m.y_pos()],[ego.x_pos(),ego.y_pos()])
    
    def manhattan_ghost(self,ego,g):
        distances = []
        for ghost in range(len(g)):
            if g[ghost].symbol() == ego:
                ego = g[ghost]
        for ghost in g:
            if ghost.symbol() != ego.symbol():
                distances.append(cityblock([ego.x_pos(),ego.y_pos()],[ghost.x_pos(),ghost.y_pos()]))
        return np.min(distances)
    
    def check_operator(self,node,m,g,world):
        match node.get_operator():
            case 'ghost':
                return self.manhattan_ghost(self._ego,g)
            case 'pill':
                return self.manhattan_pill(m,world)
            case 'pac':
                return self.manhattan_pac(m,g)
            case 'walls':
                return self.walls(m,world)
            case 'fruit':
                return self.manhattan_fruit(m,world)
            case 'rand':
                return np.random.normal(0,np.sqrt(np.square(world.x_dim())+np.square(world.y_dim()))+1)
        