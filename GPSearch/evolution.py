# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 02:26:43 2025

@author: Alec
"""
from worldgen import World
from players import PacMan, Ghost
from play import Game
import matplotlib.pyplot as plt
import selection
import numpy as np
import mutators
import random
import copy
import os


def generate_worlds(nworlds,xdim,ydim,walld,ppill):
    worlds = []
    for w in range(nworlds):
        worlds.append(World(xdim,ydim,walld,ppill))
    return worlds

def generate_pacmen(popsize,mdepth,treesize,prob):
    pacmen = []
    for p in range(popsize):
        pacmen.append(PacMan(p,mdepth,treesize,prob))
    return pacmen

def generate_ghosts(popsize,mdepth,treesize,prob,xdim,ydim):
    ghosts = []
    for p in range(popsize):
        ghosts.append(Ghost(p,mdepth,treesize,prob,0,xdim,ydim))
    return ghosts
        
def initialize(popsize,mdepth,treesize,prob,nworlds,xdim,ydim,walld,ppill,rng_init=False):
    if isinstance(rng_init,int):
        np.random.seed(rng_init)
    worlds = generate_worlds(nworlds, xdim, ydim, walld, ppill)
    pacmen = generate_pacmen(popsize,mdepth,treesize,prob)
    ghosts = generate_ghosts(popsize,mdepth,treesize,prob,xdim,ydim)
    return worlds,pacmen,ghosts

def play_game(game,pacman,ghosts,world):
    game.play(pacman,ghosts,world)
    pacman.update_allscores(pacman.score)
    for g in ghosts:
        g.update_allscores(g.score)
    world.reset_pills()

def run_epoch(epoch,worlds,popsize,pacmen,ghosts,nghosts,fspawn,time):
    wcount = 0
    #Reset the scores before running the epoch
    for i in range(popsize):
        pacmen[i].allscores = []
        ghosts[i].allscores = []
    for w in worlds:
        wcount += 1
        for p in range(popsize):
            gplayers = random.sample(ghosts,nghosts)
            for i in range(nghosts):
                gplayers[i].symbol = i + 1
                gplayers[i].allscores = []
            fname = 'worldfiles/epoch'+str(epoch)+'/player'+str(pacmen[p].identifier)+'/world'+str(wcount)+'.txt'
            os.makedirs(os.path.dirname(fname), exist_ok=True)
            game = Game(fspawn,time,fname) 
            play_game(game,pacmen[p],gplayers,w)

def generate_children(players,popsize,parents,idno):
    i = 0
    while i < (popsize-parents):
        #Crossover
        if bool(random.getrandbits(1)) and i < (popsize-parents)-1:
            i+=1
            p1,p2 = random.choices(players,k=2)
            p1 = copy.deepcopy(p1)
            p2 = copy.deepcopy(p2)
            o1,o2 = mutators.crossover(p1.controller.tree, p2.controller.tree)
            p1.controller.tree = o1
            p1.controller.tree.reset_order()
            p1.controller.tree.update_order(p1.controller.tree.root)
            p2.controller.tree = o2
            p2.controller.tree.reset_order()
            p2.controller.tree.update_order(p2.controller.tree.root)
            p1.identifier = idno + 1
            p2.identifier = idno + 2
            players.append(p1)
            players.append(p2)
            idno += 2
        #Point Mutations
        else:
            p1 = copy.deepcopy(random.choice(players))
            p1.controller.tree = mutators.point_mutation(p1.controller.tree)
            p1.controller.tree.reset_order()
            p1.controller.tree.update_order(p1.controller.tree.root)
            p1.identifier = idno + 1
            idno += 1
            players.append(p1)
        i+=1
    return idno
        
def run(nworlds,popsize,mdepth,lsize,tprob,xdim,ydim,wden,ppill,rnginit,nghosts,fprob,gtime,clim,parents,epochs,sel,evghosts):
    worlds,pacmen,ghosts = initialize(popsize,mdepth,lsize,tprob,nworlds,xdim,ydim,wden,ppill)
    bestruns = []
    pacid= ghostid = popsize
    for i in range(epochs):
        print('Epoch: ' + str(i+1))
        run_epoch(i,worlds,popsize, pacmen, ghosts,nghosts,fprob,gtime)
        bestp = 0
        bestscore = 0
        best = ''
        pacmen = selection.truncsel(pacmen, clim)
        for p in pacmen:
            avgscore = np.mean(p.allscores)
            if avgscore > bestscore:
                bestscore = avgscore
                best = p.allscores
                bestp = p.identifier
        print('Best Score: ' + str(avgscore))
        print('At: ' + str(bestp))
        bestruns.append(best)
        if sel == 'ktournament':
            pacmen = selection.ktournament(pacmen,parents,parents)
        else:
            pacmen = selection.fitpropsel(pacmen,parents)
        pacid = generate_children(pacmen, popsize, parents,pacid)
        if evghosts:
            ghosts = selection.truncsel(ghosts,clim)
            if sel == 'ktournament':
                ghosts = selection.ktournament(ghosts,parents,parents)
            else:
                ghosts = selection.fitpropsel(ghosts,parents)
            for p in pacmen:
                p.allscores = []
            for g in ghosts:
                g.allscores = []
            ghostid = generate_children(ghosts,popsize,parents,ghostid)
    plt.violinplot(bestruns)
    plt.boxplot(bestruns)
    plt.show()