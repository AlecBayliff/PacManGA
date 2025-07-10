# -*- coding: utf-8 -*-
"""
Created on Wed Jul  9 22:20:59 2025

@author: Alec
"""
import tree
import copy
import numpy as np
from PrettyPrint import PrettyPrintTree

def crossover(treeA,treeB):
    #Create copies of tree A and B
    copyA = copy.deepcopy(treeA)
    copyB = copy.deepcopy(treeB)
    #Get the roots of each tree
    rootA = copyA.get_root()
    rootB = copyB.get_root()
    #Get the nonterminals to select a crossover point
    ntermsA = treeA.get_nonterminals()
    ntermsB = treeB.get_nonterminals()
    if ntermsA:
        selectA = ntermsA[np.random.randint(0,len(ntermsA))]
    else:
        selectA = 0
    if ntermsB:
        selectB = ntermsB[np.random.randint(0,len(ntermsB))]
    else:
        selectB = 0
    #Find the crossover node
    subtreeA = copy.deepcopy(find_node(rootA,selectA))
    subtreeB = copy.deepcopy(find_node(rootB,selectB))
    #Perform the crossover
    replace_node(rootA,subtreeB,selectA)
    replace_node(rootB,subtreeA,selectB)
    #Update the new trees accordingly
    copyA.reset_order()
    copyA.update_order(copyA.get_root())
    copyB.reset_order()
    copyB.update_order(copyB.get_root())
    return [copyA,copyB]

    
def find_node(node,num):
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
        node = find_node(children[count],num)
        return node
    
def replace_node(node,rep,num):
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
        replace_node(children[count],rep,num)
            
treeA = tree.PacTree(2,3,0.5)
treeB = tree.PacTree(2,3,0.1)
pt = PrettyPrintTree(lambda x: x._children, lambda x: x._operator)
print('Tree A:')
pt(treeA.get_root())
print('Tree B: ')
pt(treeB.get_root())
crossA,crossB = crossover(treeA,treeB)
print('Tree A:')
pt(treeA.get_root())
print('Cross A:')
pt(crossA.get_root())