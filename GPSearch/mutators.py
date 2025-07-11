# -*- coding: utf-8 -*-
"""
Created on Wed Jul  9 22:20:59 2025

@author: Alec
"""
import tree
import copy
import numpy as np
import random
from PrettyPrint import PrettyPrintTree

def crossover(treeA,treeB):
    #Create copies of tree A and B
    copyA = copy.deepcopy(treeA)
    copyB = copy.deepcopy(treeB)
    
    #Get the roots of each tree
    rootA = copyA.get_root()
    rootB = copyB.get_root()
    
    #Get the nonterminals to select a crossover point
    ntermsA = copyA.get_nonterminals()
    ntermsB = copyB.get_nonterminals()
    selectA = random.choice(ntermsA)
    selectB = random.choice(ntermsB)
    
    #Find the crossover node
    subtreeA = copy.deepcopy(copyA.find_node(rootA,selectA))
    subtreeB = copy.deepcopy(copyB.find_node(rootB,selectB))
    
    #Perform the crossover
    copyA.replace_node(rootA,subtreeB,selectA)
    copyB.replace_node(rootB,subtreeA,selectB)
    
    #Update the new trees accordingly
    copyA.reset_order()
    copyA.update_order(copyA.get_root())
    copyB.reset_order()
    copyB.update_order(copyB.get_root())
    return [copyA,copyB]

def translocation(tree):
    root = tree.get_root()
    #Handle the case where root is the only terminal
    if len(tree.get_nonterminals()) == 1:
        children = copy.deepcopy(root.get_children())
        nodeA = random.choice(children)
        nodeB = random.choice(children)
        if nodeA.get_order() == nodeB.get_order():
            while(nodeA.get_order() == nodeB.get_order()):
                nodeB = random.choice(children)
        tree.replace_node(root,nodeA,nodeB.get_order())
        tree.replace_node(root,nodeB,nodeA.get_order())
        tree.reset_order()
        tree.update_order(root)
        return tree
            
    tornt = bool(random.getrandbits(1))
    if tornt:
        select = tree.get_nonterminals()
    else:
        select = tree.get_terminals()
    selectA = random.choice(select)
    selectB = random.choice(select)
    if selectA == selectB:
        while selectB == selectA:
            selectB = random.choice(select)
    subtreeA = copy.deepcopy(tree.find_node(root,selectA))
    subtreeB = copy.deepcopy(tree.find_node(root,selectB))
    tree.replace_node(root,subtreeB,selectA)
    tree.replace_node(root,subtreeA,selectB)
    tree.reset_order()
    tree.update_order(root)
    return tree
    

        
def point_mutation(tree):
    copytree = copy.deepcopy(tree)
    #Select whether or not to mutate terminal or nonterminal nodes
    tornt = bool(random.getrandbits(1))
    if tornt:
        select = copytree.get_nonterminals()
    else:
        select = copytree.get_terminals()
    select = random.choice(select)
    choice = random.choice(['ins','del','mut','trans'])
    #Don't allow deletion if there is only a single nonterminal
    if choice == 'del' and len(copytree.get_nonterminals()) == 1:
        while choice == 'del':
            choice = random.choice(['ins','del','mut','trans'])
    match choice:
        #Instert a random tree
        case 'ins':
            copytree.insert(select)
            return copytree
        #Delete a node
        case 'del':
            #Don't delete the root or terminals
            if select == 0 or select in copytree.get_terminals():
                select = random.choice(copytree.get_nonterminals())
                while select == 0:
                    select = random.choice(copytree.get_nonterminals())
            copytree.prune(copytree.get_root(),select)
            return copytree
        #Mutate a node
        case 'mut':
            node = copytree.find_node(copytree.get_root(),select)
            current = node.get_operator()
            #Check if terminal or nonterminal and change the operator
            if node.check_terminal():
                while(node.get_operator() == current):
                    node.set_operator(node.select_op_t())
            else:
                while(node.get_operator() == current):
                    node.set_operator(node.select_op_nt())
            return copytree
        #Replace a node with a subtree from the tree
        case 'trans':
            return translocation(copytree)
            
    
            
treeA = tree.PacTree(3,2,0.1)
treeB = tree.PacTree(3,2,0.1)
pt = PrettyPrintTree(lambda x: x._children, lambda x: x._operator)
print('Tree A:')
pt(treeA.get_root())
#print('Tree B: ')
#pt(treeB.get_root())
for x in range(1000):
    transA = point_mutation(treeA)
#print('Tree A:')
#pt(treeA.get_root())
print('Trans A:')
pt(transA.get_root())