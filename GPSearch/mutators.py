# -*- coding: utf-8 -*-
"""
Created on Wed Jul  9 22:20:59 2025

@author: Alec
"""
import copy
import random

def crossover(treeA,treeB):
    #Create copies of tree A and B
    copyA = copy.deepcopy(treeA)
    copyB = copy.deepcopy(treeB)
    
    #Get the roots of each tree
    rootA = copyA.root
    rootB = copyB.root
    
    #Get the nonterminals to select a crossover point
    ntermsA = copyA.nonterminals
    ntermsB = copyB.nonterminals
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
    copyA.update_order(copyA.root)
    copyB.reset_order()
    copyB.update_order(copyB.root)
    return [copyA,copyB]

def translocation(tree):
    root = tree.root
    #Handle the case where root is the only terminal
    if len(tree.nonterminals) == 1:
        children = copy.deepcopy(root.children)
        nodeA = random.choice(children)
        nodeB = random.choice(children)
        if nodeA.order == nodeB.order:
            while(nodeA.order == nodeB.order):
                nodeB = random.choice(children)
        tree.replace_node(root,nodeA,nodeB.order)
        tree.replace_node(root,nodeB,nodeA.order)
        tree.reset_order()
        tree.update_order(root)
        return tree
            
    if bool(random.getrandbits(1)):
        select = tree.nonterminals
    else:
        select = tree.terminals
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
    if bool(random.getrandbits(1)):
        select = copytree.nonterminals
    else:
        select = copytree.terminals
    select = random.choice(select)
    choice = random.choice(['ins','del','mut','trans'])
    #Don't allow deletion if there is only a single nonterminal
    if choice == 'del' and len(copytree.nonterminals) == 1:
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
            if select == 0 or select in copytree.terminals:
                select = random.choice(copytree.nonterminals)
                while select == 0:
                    select = random.choice(copytree.nonterminals)
            copytree.prune(copytree.root,select)
            return copytree
        #Mutate a node
        case 'mut':
            node = copytree.find_node(copytree.root,select)
            current = node.operator
            #Check if terminal or nonterminal and change the operator
            if node.check_terminal():
                while(node.operator == current):
                    node.operator = node.select_op_t()
            else:
                while(node.operator == current):
                    node.operator = node.select_op_nt()
            return copytree
        #Replace a node with a subtree from the tree
        case 'trans':
            return translocation(copytree)