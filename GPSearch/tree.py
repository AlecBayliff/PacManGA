#Alec Bayliff
import numpy as np
from PrettyPrint import PrettyPrintTree

class Tree:
    def __init__(self):
        self._norder = 0
        self._nonterminals = [0]
        self._terminals = []

    class Node:
        def __init__(self,op=None,children=[],depth=0,mdepth=1,size=2,order=0):
            self._children = children
            self._operator = op
            self._order = order
            
        @property
        def children(self):
            if self._children:
                return self._children
            else:
                return False
            
        @children.setter
        def children(self,children):
            self._children = []
            for child in children:
                self._children.append(child)
        
        @property
        def operator(self):
            return self._operator
        
        @operator.setter
        def operator(self,operator):
            self._operator = operator
            
        @property
        def order(self):
            return self._order
            
        @order.setter
        def order(self,order):
            self._order = order
                
        def print_node(self):
            count = 0
            if self._children:
                for c in self._children:
                    count += 1
            print('Children: ' + str(count))
            print(self._operator)
            print(self._order)
        
    @property
    def terminals(self):
        return self._terminals
    
    @property
    def nonterminals(self):
        return self._nonterminals
        
    @property
    def root(self):
        return self._root
    
    @root.setter
    def root(self,node):
        self._root = node
        
    def print_tree(self):
        pt = PrettyPrintTree(lambda x: x._children, lambda x: x._operator)
        pt(self._root)
    
    def inc_order(self):
        self._norder += 1
            
    def prune(self,node,select):
        if node.order == select and node.children:
            self.delete_nodes(node)
            return True
        else:
            children = node.children
            pruned = False
            if children:
                for child in node.children:
                    if self.prune(child,select):
                        children = node.children
                        for c in range(len(children)):
                            if children[c].order == select:
                                pruned = c
                        children.pop(pruned)

                #If there are not enough children for a nonterminal operation, move child up.
                if node.check_terminal() == False and len(children) < 2:
                    node.operator = children[0].operator
                    for child in children:
                        if child.children:
                            node.children = child.children
            self.reset_order()
            self.update_order(self.root)
            
    def find_node(self,node,num):
        #If root is the node we're looking for, return it
        if node.order == num:
            return node
        
        #Otherwise, proceed to search for the node
        children = node.children
        if children:
            count = -1
            for child in children:
                if child.order < num:
                    count += 1
                elif child.order == num:
                    return child
            node = self.find_node(children[count],num)
            return node
        
    def replace_node(self,node,rep,num):
        if num == 0:
            node.children = rep.children
            node.operator = rep.operator
            return
        children = node.children
        if children:
            count = -1
            for child in children:
                if child.order < num:
                    count += 1
                elif child.order == num:
                    if rep.children:
                        child.children = rep.children
                    else:
                        rep.children = []
                    child.operator = rep.operator
                    return
            self.replace_node(children[count],rep,num)

    def delete_nodes(self,node):
        children = node.children
        if children:
            for child in children:
                self.delete_nodes(child)
            children.clear()
    
    def update_order(self,node):
        self._terminals = []
        self._nonterminals = [0]
        node.order = self._norder
        children = node.children
        if children:
            for child in children:
                self.inc_order()
                if child.children:
                    self._nonterminals.append(self._norder)
                self.update_order(child)
        else:
            self._terminals.append(self._norder)
            
    def reset_order(self):
        self._norder = 0
        

class PacTree(Tree):
    def __init__(self,mdepth=1,size=2,prob=0):
        Tree.__init__(self)
        self._size = size
        self._prob = prob
        self._root = self.PacNode(depth=0,mdepth=mdepth)
        self.grow(self._root,0,mdepth,prob,0)
        
    def grow(self,node,depth,mdepth,prob,order):
        #If at max depth, set terminal children
        if depth == mdepth:
            children = []
            for i in range(self._size):
                self.inc_order()
                self._terminals.append(self._norder)
                children.append(self.PacNode(op=node.select_op_t(),children=[],depth=depth+1,order=self._norder))
            node.children = children
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
                    self.inc_order()
                    self._terminals.append(self._norder)
                    children.append(self.PacNode(op=node.select_op_t(),children=[],depth=depth+1,order=self._norder))
            else:
                for i in range(count):
                    self.inc_order()
                    self._nonterminals.append(self._norder)
                    child = self.PacNode(op=node.select_op_nt(),children=[],depth=depth+1,mdepth=mdepth,order=self._norder)
                    self.grow(child,depth+1,mdepth,prob,self._norder)
                    children.append(child)
            node.children = children
            
    def insert(self,num):
        newtree = PacTree(mdepth=2,size=self._size,prob=self._prob)
        self.replace_node(self.root, newtree.root, num)
        
    class PacNode(Tree.Node):
        def __init__(self,op=None,children=[],depth=0,mdepth=1,size=2,order=0):
            self._children = children
            if op:
                self._operator = op
            else:
                self._operator = self.select_op_nt()
            self._order = order
            self._depth = depth
            
        def check_terminal(self):
            terminals = {'ghost','pill','walls','fruit','rand'}
            if self.operator in terminals:
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
        Tree.__init__(self)
        self._size = size
        self._prob = prob
        self._root = self.GhostNode(depth=0,mdepth=mdepth)
        self.grow(self._root,0,mdepth,prob,0)
        
    def grow(self,node,depth,mdepth,prob,order):
        #If at max depth, set terminal children
        if depth == mdepth:
            children = []
            for i in range(self._size):
                self.inc_order()
                self._terminals.append(self._norder)
                children.append(self.GhostNode(op=node.select_op_t(),children=[],depth=depth+1,order=self._norder))
            node.children = children
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
                    self.inc_order()
                    self._terminals.append(self._norder)
                    children.append(self.GhostNode(op=node.select_op_t(),children=[],depth=depth+1,order=self._norder))
            else:
                for i in range(count):
                    self.inc_order()
                    self._nonterminals.append(self._norder)
                    child = self.GhostNode(op=node.select_op_nt(),children=[],depth=depth+1,mdepth=mdepth,order=self._norder)
                    self.grow(child,depth+1,mdepth,prob,self._norder)
                    children.append(child)
            node.children = children
            
    def insert(self,num):
        newtree = GhostTree(mdepth=2,size=self._size,prob=self._prob)
        self.replace_node(self.root, newtree.root, num)
    
    class GhostNode(Tree.Node):
        def __init__(self,op=None,children=[],depth=0,mdepth=1,size=2,order=0):
            self._children = children
            if op:
                self._operator = op
            else:
                self._operator = self.select_op_nt()
            self._order = order
            self._depth = depth
            
        def check_terminal(self):
            terminals = {'ghost','pill','pac','walls','fruit','rand'}
            if self.operator in terminals:
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