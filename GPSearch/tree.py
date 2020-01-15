#Alec Bayliff
import numpy as np
import scipy as sp
import sys
from scipy.spatial.distance import cityblock

def manhattan_ghost(m,g):
    distances = []
    for ghost in g:
        distances.append(cityblock([m.x_pos(),m.y_pos()],[ghost.x_pos(),ghost.y_pos()]))
    return np.minimum(distances)

def manhattan_pill(m,world):
    coords = []
    for w in range(world.x_dim()):
        for z in range(world.y_dim()):
            if world.world_map[w][z] == 'p':
                coords.append([w,z])
    return sp.spatial.distance.cdist([[m.x_pos(),m.y_pos()]],coords,'cityblock').min()
    

def add(node):
    children = node.get_children()
    return np.add(children[0],children[1])

def sub(node):
    children = node.get_children()
    return np.subtract(children[0],children[1])

def mult(node):
    children = node.get_children()
    return np.multiply(children[0],children[1])

def div(node):
    children = node.get_children()
    if children[1] != 0:
        return np.divide(children[0],children[1])
    else:
        return sys.float_info.max
    
def node_rand(node):
    children = node.get_children()
    return np.random.uniform(children[0],children[1])

'''
class Node:
    def __init__(self,op,children):
        if op != 'm' and not isinstance(op,int):
            self._children = children
        else:
            self._value = 
        self._operator = op
        
        
        
    def get_children(self):
        if self._children:
            return self.children
        else:
            return False
        '''