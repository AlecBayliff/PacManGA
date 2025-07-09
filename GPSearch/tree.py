#Alec Bayliff
import numpy as np
from PrettyPrint import PrettyPrintTree

class Tree:
    norder = 0
    nonterminals = []
    terminals = []
    class Node:
        def __init__(self,op='',children=[],depth=0,mdepth=1,size=2,order=0):
            self._children = children
            self._operator = op
            self._depth = depth
            self._mdepth = mdepth
            self._size = size
            self._order = order
            
        def get_children(self):
            if self._children:
                return self._children
            else:
                return False
            
        def set_children(self,children):
            self._children = []
            for child in children:
                self._children.append(child)
                
        def set_operator(self,operator):
            self._operator = operator
            
        def set_order(self,order):
            self._order = order
                
        def get_order(self):
            return self._order
        
        def get_operator(self):
            return self._operator
        
        def get_terminals(self):
            return self.terminals
        
        def get_nonterminals(self):
            return self.nonterminals
        
    def get_root(self):
        return self._root
    
    def grow(self,node,depth,mdepth,prob,order):
        #If at max depth, set terminal children
        if depth == mdepth:
            children = []
            for i in range(self._size):
                self.norder += 1
                self.terminals.append(self.norder)
                children.append(self.Node(op=self.select_op_t(),children=[],depth=depth+1,order=self.norder))
            node.set_children(children)
        #Otherwise, grow stochastically
        else:
            children = []
            count = 0
            for i in range(self._size):
                p = np.random.rand()
                if p >= prob:
                    count += 1
            #If not enough nonterminal children are created, create a terminal children. Otherwise, proceed
            if count <= 1:
                children = []
                for i in range(self._size):
                    self.norder += 1
                    self.terminals.append(self.norder)
                    children.append(self.Node(op=self.select_op_t(),children=[],depth=depth+1,order=self.norder))
            else:
                for i in range(count):
                    self.norder += 1
                    self.nonterminals.append(self.norder)
                    child = self.Node(op=self.select_op_nt(),children=[],depth=depth+1,mdepth=mdepth,order=self.norder)
                    self.grow(child,depth+1,mdepth,prob,self.norder)
                    children.append(child)
            node.set_children(children)
            
    def prune(self,node,select):
        if node.get_order() == select and node.get_children():
            self.delete_nodes(node)
            return True
        else:
            children = node.get_children()
            pruned = False
            if children:
                for child in node.get_children():
                    if self.prune(child,select):
                        children = node.get_children()
                        for c in range(len(children)):
                            if children[c].get_order() == select:
                                pruned = c
                        children.pop(pruned)

                #If there are not enough children for a nonterminal operation, move child up.
                if self.check_terminal(node) == False and len(children) < 2:
                    node.set_operator(children[0].get_operator())
                    for child in children:
                        if child.get_children():
                            node.set_children(child.get_children())
            self.norder = 0
            self.update_order(self.get_root(),clean=True)

    def delete_nodes(self,node):
        children = node.get_children()
        if children:
            for child in children:
                self.delete_nodes(child)
            children.clear()
            
    def update_order(self,node,clean=False):
        if clean:
            self.terminals = []
            self.nonterminals = []
        node.set_order(self.norder)
        children = node.get_children()
        if children:
            for child in children:
                self.norder += 1
                if child.get_children():
                    self.nonterminals.append(self.norder)
                self.update_order(child)
        else:
            self.terminals.append(self.norder)
    

class PacTree(Tree):
    def __init__(self,mdepth=1,size=2,prob=0):
        self._size = size
        self._root = self.Node(op=self.select_op_nt(),depth=0,mdepth=mdepth)
        self.grow(self._root,0,mdepth,prob,0)
                
    def check_terminal(self,node):
        terminals = {'ghost','pill','walls','fruit','rand'}
        if node.get_operator in terminals:
            return True
        else:
            return False
    
    def select_op_nt(self):
        rnum = np.random.randint(0,5)
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
        rnum = np.random.randint(0,5)
        match rnum:
            case 0:
                return 'ghost'
            case 1:
                return 'pill'
            case 2:
                return 'walls'
            case 3:
                return 'fruit'
            case 4:
                return 'rand'

class GhostTree(Tree):
    def __init__(self,mdepth=1,size=2,prob=0):
        self._size = size
        self._root = self.Node(op=self.select_op_nt(),depth=0,mdepth=mdepth)
        self.grow(self._root,0,mdepth,prob,0)
        
    def check_terminal(self,node):
        terminals = {'ghost','pill','pac','walls','fruit','rand'}
        if node.get_operator in terminals:
            return True
        else:
            return False
    
    def select_op_nt(self):
        rnum = np.random.randint(0,5)
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
        rnum = np.random.randint(0,6)
        match rnum:
            case 0:
                return 'ghost'
            case 1:
                return 'pill'
            case 2:
                return 'pac'
            case 3:
                return 'walls'
            case 4:
                return 'fruit'
            case 5:
                return 'rand'