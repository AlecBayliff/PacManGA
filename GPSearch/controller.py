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
    def evaluate(self,pac,ghosts,world):
        controller = self.controller
        output = self.operate(controller,pac,ghosts,world)
        output = np.rint(output)
        return output
    
    def operate(self,node,m,g,world):
        children = node.children
        inputs = []
        if children:
            for child in children:
                inputs.append(self.operate(child,m,g,world))
            match node.operator:
                case '+':
                    return np.sum(inputs)
                case '-':
                    a = 0
                    for b in inputs:
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
                            #Return a number higher than the maximum distance of the world
                            return np.sqrt(np.square(world.x_dim)+np.square(world.y_dim))+1
                    return a
                case 'r':
                    rnum = np.random.randint(0,len(inputs))
                    return inputs[rnum]
        else:
            return self.check_operator(node,m,g,world)
        
    @property
    def controller(self):
        return self._controller
    
    @controller.setter
    def controller(self,controller):
        self._controller = controller
        
    @property
    def tree(self):
        return self._tree
    
    @tree.setter
    def tree(self,tree):
        self._tree = tree
        
    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self,val):
        self._size = val
        
    def manhattan_pill(self,m,world):
        return sp.spatial.distance.cdist([[m.x_pos,m.y_pos]],world.pills,'cityblock').min()
    
    def manhattan_fruit(self,player,world):
        if world.fruit:
            coords = world.fruit
            return cityblock([player.x_pos,player.y_pos],coords)
        else:
            return world.x_dim * world.y_dim

    def walls(self,m,world):
        return world.count_walls(m.x_pos,m.y_pos)
    
class PacController(Controller):
    def __init__(self,mdepth,size,prob):
        self._tree = PacTree(mdepth,size,prob)
        self._controller = self._tree.root
        self._size = self._tree.terminals[-1]+1
                
    def manhattan_ghost(self,m,g):
        distances = []
        for ghost in g:
            distances.append(cityblock([m.x_pos,m.y_pos],[ghost.x_pos,ghost.y_pos]))
        return np.min(distances)
    
    def check_operator(self,node,m,g,world):
        match node.operator:
            case 'ghost':
                return self.manhattan_ghost(m,g)
            case 'pill':
                return self.manhattan_pill(m,world)
            case 'walls':
                return self.walls(m,world)
            case 'fruit':
                return self.manhattan_fruit(m,world)
            case 'rand':
                return np.random.normal(0,np.sqrt(np.square(world.x_dim)+np.square(world.y_dim))+1)
                
class GhostController(Controller):
    def __init__(self,mdepth,size,prob,ego):
        self._tree = GhostTree(mdepth,size,prob)
        self._controller = self._tree.root
        self._size = self._tree.terminals[-1]+1
        self._ego = ego
        
    @property
    def ego(self):
        return self._ego
    @ego.setter
    def ego(self,ego):
        self._ego = ego
                
    def manhattan_pac(self,m,g):
        return cityblock([m.x_pos,m.y_pos],[g.x_pos,g.y_pos])
    
    def manhattan_ghost(self,g):
        distances = []
        for ghost in g:
            if ghost.symbol == self._ego:
                ego = ghost
        for ghost in g:
            if ghost.symbol != self._ego:
                distances.append(cityblock([ego.x_pos,ego.y_pos],[ghost.x_pos,ghost.y_pos]))
        return np.min(distances)

    
    def check_operator(self,node,m,g,world):
        match node.operator:
            case 'ghost':
                return self.manhattan_ghost(g)
            case 'pill':
                return self.manhattan_pill(m,world)
            case 'pac':
                return self.manhattan_pac(m,g[self._ego-1])
            case 'walls':
                return self.walls(m,world)
            case 'fruit':
                return self.manhattan_fruit(m,world)
            case 'rand':
                return np.random.normal(0,np.sqrt(np.square(world.x_dim)+np.square(world.y_dim))+1)