# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 02:26:43 2025

@author: Alec
"""
from worldgen import World
from players import PacMan, Ghost
from play import Game
import numpy as np
import random

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
        fname = 'world'+str(wcount)+'.txt'
        wcount += 1
        game = Game(fspawn,time,fname,nghosts)
        for p in range(popsize):
            gplayers = random.sample(ghosts,nghosts)
            for x in range(nghosts):
                gplayers[x].symbol = x + 1
            game.play(pacmen[p],gplayers,w)
            w.reset_pills()