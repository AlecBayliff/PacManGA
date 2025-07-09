# -*- coding: utf-8 -*-
"""
Created on Tue Jul  8 18:30:30 2025

@author: Alec
"""
import numpy as np
from tree import PacTree
import scipy as sp
import sys
from scipy.spatial.distance import cityblock

class PacController:
    def __init__(self,mdepth,size,prob):
        self._controller = PacTree(mdepth,size,prob).get_root()
        
    def evaluate(self,pac,ghost,world):
        controller = self.get_controller()
        output = self.operate(controller,pac,ghost,world)
        output = np.rint(output)
        return output
        
    def get_controller(self):
        return self._controller
    
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
                            return sys.float_info.max
                    return a
                case 'r':
                    rnum = np.random.randint(0,len(inputs))
                    return inputs[rnum]
            
        else:
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
                    return np.random.normal(0,100)
        
    def manhattan_ghost(self,m,g):
        distances = []
        for ghost in g:
            distances.append(cityblock([m.x_pos(),m.y_pos()],[ghost.x_pos(),ghost.y_pos()]))
        return np.min(distances)

    def manhattan_pill(self,m,world):
        coords = []
        for w in range(world.x_dim()):
            for z in range(world.y_dim()):
                if world.world_map[w][z] == 'p':
                    coords.append([w,z])
        return sp.spatial.distance.cdist([[m.x_pos(),m.y_pos()]],coords,'cityblock').min()
    
    def manhattan_fruit(self,m,world):
        coords = []
        if world.is_fruit():
            for w in range(world.x_dim()):
                for z in range(world.y_dim()):
                    if world.world_map[w][z] == 'f':
                        coords.append([w,z])
            return sp.spatial.distance.cdist([[m.x_pos(),m.y_pos()]],coords,'cityblock').min()
        else:
            return world.x_dim() * world.y_dim()

    def walls(self,m,world):
        count = 0
        if m.x_pos()-1 == 'w':
            count += 1
        if m.x_pos()+1 == 'w':
            count += 1
        if m.y_pos()-1 == 'w':
            count += 1
        if m.y_pos()+1 == 'w':
            count += 1
        return count