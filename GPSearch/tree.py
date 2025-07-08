#Alec Bayliff
import numpy as np
import scipy as sp
import sys
from scipy.spatial.distance import cityblock
from PrettyPrint import PrettyPrintTree

class PacTree:
    def __init__(self,mdepth=1,size=2,prob=0):
        #Size = size-1 because we start with zero
        self._size = size
        self._root = self.Node(op=self.select_op_nt(),depth=0,mdepth=mdepth)
        self.grow(self._root,0,mdepth,prob)
        
    def get_root(self):
        return self._root
    
    def grow(self,node,depth,mdepth,prob):
        #If at max depth, set nonterminal children
        if depth == mdepth:
            children = []
            for i in range(self._size):
                children.append(self.Node(op=self.select_op_t(),children=[],depth=depth))
            node.set_children(children)
        #Otherwise, grow stochastically
        else:
            children = []
            count = 0
            for i in range(self._size):
                p = np.random.rand()
                if p >= prob:
                    count += 1
                    child = self.Node(op=self.select_op_nt(),children=[],depth=depth,mdepth=mdepth)
                    self.grow(child,depth+1,mdepth,prob)
                    children.append(child)
            #If no nonterminal children are created, create a terminal child
            if count <= 1:
                children = []
                for i in range(self._size):
                    children.append(self.Node(op=self.select_op_t(),children=[],depth=depth))
            node.set_children(children)
        
    def select_op_nt(self):
        rnum = np.random.randint(0,4)
        match rnum:
            case 0:
                return '+'
            case 1:
                return '-'
            case 2:
                return '*'
            case 3:
                return '/'
            case 4:
                return 'r'

    def select_op_t(self):
        rnum = np.random.randint(0,3)
        match rnum:
            case 0:
                return 'ghost'
            case 1:
                return 'pill'
            case 2:
                return 'walls'
            case 3:
                return 'fruit'
            
    class Node:
        def __init__(self,op='',children=[],depth=0,mdepth=1,size=2):
            self._children = children
            self._operator = op
            self._depth = depth
            self._mdepth = mdepth
            self._size = size
            
        def get_children(self):
            if self._children:
                return self._children
            else:
                return False
            
        def set_children(self,children):
            for child in children:
                self._children.append(child)

def test_tree():
    test = PacTree(mdepth=3,size=2,prob=.15)
    return test

x = test_tree()
z = x.get_root()
pt = PrettyPrintTree(lambda z: z._children, lambda z: z._operator)
pt(x.get_root())

'''
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

    def walls(m,world):
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