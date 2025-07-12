#Alec Bayliff
import numpy as np

class Tree:
    def __init__(self):
        self._norder = 0
        self._nonterminals = [0]
        self._terminals = []

    class Node:
        def __init__(self,op=None,children=[],depth=0,mdepth=1,size=2,order=0):
            self._children = children
            self._operator = op
            #self._depth = depth
            #self._mdepth = mdepth
            #self._size = size
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
        return self._terminals
    
    def get_nonterminals(self):
        return self._nonterminals
        
    def get_root(self):
        return self._root
    
    def inc_order(self):
        self._norder += 1
            
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
                if node.check_terminal() == False and len(children) < 2:
                    node.set_operator(children[0].get_operator())
                    for child in children:
                        if child.get_children():
                            node.set_children(child.get_children())
                            
            self.reset_order()
            self.update_order(self.get_root())
            
            
    def find_node(self,node,num):
        #If root is the node we're looking for, return it
        if node.get_order() == num:
            return node
        
        #Otherwise, proceed to search for the node
        children = node.get_children()
        if children:
            count = -1
            for child in children:
                if child.get_order() < num:
                    count += 1
                elif child.get_order() == num:
                    return child
            node = self.find_node(children[count],num)
            return node
        
    def replace_node(self,node,rep,num):
        if num == 0:
            node.set_children(rep.get_children())
            node.set_operator(rep.get_operator())
            return
        children = node.get_children()
        if children:
            count = -1
            for child in children:
                if child.get_order() < num:
                    count += 1
                elif child.get_order() == num:
                    if rep.get_children():
                        child.set_children(rep.get_children())
                    else:
                        rep.set_children([])
                    child.set_operator(rep.get_operator())
                    return
            self.replace_node(children[count],rep,num)

    def delete_nodes(self,node):
        children = node.get_children()
        if children:
            for child in children:
                self.delete_nodes(child)
            children.clear()
    
    def update_order(self,node):
        self._terminals = []
        self._nonterminals = [0]
        node.set_order(self._norder)
        children = node.get_children()
        if children:
            for child in children:
                self.inc_order()
                if child.get_children():
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
        self._root = self.PacNode(depth=0,mdepth=mdepth)
        self.grow(self._root,0,mdepth,prob,0)
        self._prob = prob
        
    def grow(self,node,depth,mdepth,prob,order):
        #If at max depth, set terminal children
        if depth == mdepth:
            children = []
            for i in range(self._size):
                self.inc_order()
                self._terminals.append(self._norder)
                children.append(self.PacNode(op=node.select_op_t(),children=[],depth=depth+1,order=self._norder))
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
            node.set_children(children)
            
    def insert(self,num):
        newtree = PacTree(mdepth=2,size=self._size,prob=self._prob)
        self.replace_node(self.get_root(), newtree.get_root(), num)
        
    class PacNode(Tree.Node):
        def __init__(self,op=None,children=[],depth=0,mdepth=1,size=2,order=0):
            self._children = children
            if op:
                self._operator = op
            else:
                self._operator = self.select_op_nt()
            #self._depth = depth
            #self._mdepth = mdepth
            #self._size = size
            self._order = order
        def check_terminal(self):
            terminals = {'ghost','pill','walls','fruit','rand'}
            if self.get_operator() in terminals:
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
        self._root = self.GhostNode(depth=0,mdepth=mdepth)
        self.grow(self._root,0,mdepth,prob,0)
        self._prob = prob
        
    def grow(self,node,depth,mdepth,prob,order):
        #If at max depth, set terminal children
        if depth == mdepth:
            children = []
            for i in range(self._size):
                self.inc_order()
                self._terminals.append(self._norder)
                children.append(self.GhostNode(op=node.select_op_t(),children=[],depth=depth+1,order=self._norder))
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
            node.set_children(children)
            
    def insert(self,num):
        newtree = PacTree(m_depth=2,size=self._size,prob=self._prob)
        self.replace_node(self.get_root(), newtree.get_root(), num)
    
    class GhostNode(Tree.Node):
        def check_terminal(self):
            terminals = {'ghost','pill','pac','walls','fruit','rand'}
            if self.get_operator() in terminals:
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