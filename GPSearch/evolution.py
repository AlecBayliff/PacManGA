# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 02:26:43 2025

@author: Alec
"""
from worldgen import World
from players import PacMan, Ghost
from play import Game
import selection
import numpy as np
import mutators
import random
import copy

def generate_worlds(nworlds,xdim,ydim,walld,ppill):
    worlds = []
    for w in range(nworlds):
        worlds.append(World(xdim,ydim,walld,ppill))
    return worlds

def generate_pacmen(popsize,mdepth,treesize,prob):
    pacmen = []
    for p in range(popsize):
        pacmen.append(PacMan(mdepth,treesize,prob))
    return pacmen

def generate_ghosts(popsize,mdepth,treesize,prob,xdim,ydim):
    ghosts = []
    for p in range(popsize):
        ghosts.append(Ghost(mdepth,treesize,prob,0,xdim,ydim))
    return ghosts
        
def initialize(popsize,mdepth,treesize,prob,nworlds,xdim,ydim,walld,ppill,rng_init=False):
    if isinstance(rng_init,int):
        np.random.seed(rng_init)
    worlds = generate_worlds(nworlds, xdim, ydim, walld, ppill)
    pacmen = generate_pacmen(popsize,mdepth,treesize,prob)
    ghosts = generate_ghosts(popsize,mdepth,treesize,prob,xdim,ydim)
    return worlds,pacmen,ghosts

def run_epoch(worlds,popsize,pacmen,ghosts,nghosts,fspawn,time):
    wcount = 0
    for w in worlds:
        print('Running World '+ str(wcount))
        fname = 'worldfiles/world'+str(wcount)+'.txt'
        wcount += 1
        game = Game(fspawn,time,fname)
        for p in range(popsize):
            gplayers = random.sample(ghosts,nghosts)
            for i in range(nghosts):
                gplayers[i].symbol = i + 1
            game.play(pacmen[p],gplayers,w)
            pacmen[p].update_allscores(pacmen[p].score)
            for g in gplayers:
                g.update_allscores(g.score)
            w.reset_pills()
            
def generate_children(pacmen,popsize,parents):
    i = 0
    while i < (popsize-parents):
        #Crossover
        if bool(random.getrandbits(1)) and i < (popsize-parents)-1:
            i+=1
            p1,p2 = random.choices(pacmen,k=2)
            p1 = copy.deepcopy(p1)
            p2 = copy.deepcopy(p2)
            o1,o2 = mutators.crossover(p1.controller.tree, p2.controller.tree)
            p1.controller.tree = o1
            p1.controller.tree.reset_order()
            p1.controller.tree.update_order(p1.controller.tree.root)
            p2.controller.tree = o2
            p2.controller.tree.reset_order()
            p2.controller.tree.update_order(p2.controller.tree.root)
            pacmen.append(p1)
            pacmen.append(p2)
        #Point Mutations
        else:
            p1 = copy.deepcopy(random.choice(pacmen))
            p1.controller.tree = mutators.point_mutation(p1.controller.tree)
            p1.controller.tree.reset_order()
            p1.controller.tree.update_order(p1.controller.tree.root)
            pacmen.append(p1)
        i+=1
        
def run(nworlds,popsize,mdepth,lsize,tprob,xdim,ydim,wden,ppill,rnginit,nghosts,fprob,gtime,clim,parents,epochs,sel):
    worlds,pacmen,ghosts = initialize(popsize,mdepth,lsize,tprob,nworlds,xdim,ydim,wden,ppill)
    for i in range(epochs):
        print('Epoch: ' + str(i+1))
        run_epoch(worlds,popsize, pacmen, ghosts,nghosts,fprob,gtime)
        pacmen = selection.truncsel(pacmen, clim)
        if sel == 'ktournament':
            pacmen = selection.ktournament(pacmen,parents,parents)
        else:
            pacmen = selection.fitpropsel(pacmen,parents)
        generate_children(pacmen, popsize, parents)
        ghosts = selection.truncsel(ghosts,clim)
        if sel == 'ktournament':
            ghosts = selection.ktournament(ghosts,parents,parents)
        else:
            ghosts = selection.fitpropsel(ghosts,parents)
        generate_children(ghosts,popsize,parents)