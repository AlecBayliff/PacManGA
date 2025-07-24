# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 02:26:43 2025

@author: Alec
"""
from worldgen import World
from players import PacMan, Ghost
from play import Game
import multiprocessing as mp
import matplotlib.pyplot as plt
import selection
import shutil
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
        np.random.default_rng(seed=rng_init)
    worlds = generate_worlds(nworlds, xdim, ydim, walld, ppill)
    pacmen = generate_pacmen(popsize,mdepth,treesize,prob)
    ghosts = generate_ghosts(popsize,mdepth,treesize,prob,xdim,ydim)
    return worlds,pacmen,ghosts

'''
This function looks a bit weird, but multiprocessing creates unique copies of variables passed in.
Ghosts, gplayers, and ghostdict all contain references to the same objects. Updating gplayers
will update the same ghost in ghosts and ghostdict. They do need to be returned out of the pool
in order to update the original copies of them, though. game.play runs faster than overhead from mp.
'''
def run_world(popsize,fspawn,t,pacmen,ghosts,nghosts,ghostdict,world,wcount,epoch):
    pacscores = []
    sumlen = 0
    k = 0
    for p in range(popsize):
        gplayers = random.sample(ghosts,nghosts)
        for i in range(nghosts):
            gplayers[i].symbol = i + 1
        fname = 'worldfiles/epoch'+str(epoch+1)+'/player'+str(pacmen[p].identifier)+'/world'+str(wcount)+'.txt'
        os.makedirs(os.path.dirname(fname), exist_ok=True)
        game = Game(fspawn,t,fname) 
        game.play(pacmen[p],gplayers,world)
        world.reset_pills()
        pacscores.append(pacmen[p].score)
        for g in gplayers:
            k+=1
            g.update_allscores(g.score)
    for g,v in ghostdict.items():
        sumlen += len(ghostdict[g].allscores)
    return pacscores,ghostdict

def run_epoch(epoch,worlds,popsize,pacmen,ghosts,nghosts,fspawn,t):
    wcount = 0
    ghostdict = {}
    wait = []
    pool = mp.Pool()
    #Reset the scores before running the epoch
    for i in range(popsize):
        pacmen[i].allscores = []
        ghosts[i].allscores = []
        ghostdict[ghosts[i].identifier] = ghosts[i]
    for w in worlds:
        wcount += 1
        wait.append(pool.apply_async(run_world,args=[popsize,fspawn,t,pacmen,ghosts,nghosts,ghostdict,w,wcount,epoch]))
    for w in wait:
        pacresults,ghostresults = w.get()
        for p in range(popsize):
            pacmen[p].update_allscores(pacresults[p])
        for g,v in ghostresults.items():
            ghostdict[g].update_allscores(v.allscores)
    pool.close()
    pool.join()

def generate_children(select,players,popsize,survivors,k,idno,mdepth,lsize,tprob,xdim=0,ydim=0):
    i = 0
    newplayers = []
    while i < (popsize-survivors):
        choice = np.random.randint(0,5)
        #Crossover
        if choice < 2 and i < (popsize-survivors)-1:
            i+=1
            if select == 'ktournament':
                p1,p2 = selection.ktournament(players, 2, k,replacement=True)
            elif select == 'fitprop':
                p1,p2 = selection.fitpropsel(players, 2)
            else:
                raise(print('Incorrect selection method!'))
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
            p1.size = p1.controller.tree.terminals[-1]+1
            p2.identifier = idno + 2
            p2.size = p2.controller.tree.terminals[-1]+1
            newplayers.append(p1)
            newplayers.append(p2)
            idno += 2
        #Point Mutations
        elif choice < 4:
            if select == 'ktournament':
                p1 = selection.ktournament(players, 1, k,replacement=True)
            elif select == 'fitprop':
                p1 = selection.fitpropsel(players, 1)
            else:
                raise(print('Incorrect selection method!'))
            p1 = copy.deepcopy(random.choice(players))
            p1.controller.tree = mutators.point_mutation(p1.controller.tree)
            p1.controller.tree.reset_order()
            p1.controller.tree.update_order(p1.controller.tree.root)
            idno += 1
            p1.identifier = idno
            p1.size = p1.controller.tree.terminals[-1]+1
            newplayers.append(p1)
        else:
            #A mircale! A genetically distinct individual is born!
            if players[0].symbol == 'm':
                idno += 1
                newplayers.append(PacMan(idno,mdepth,lsize,tprob))
            else:
                idno += 1
                newplayers.append(Ghost(idno,mdepth,lsize,tprob,0,xdim,ydim))
        i+=1
    players.extend(newplayers)
    return idno
        
def run(nworlds,popsize,mdepth,lsize,tprob,xdim,ydim,wden,ppill,rnginit,nghosts,fprob,gtime,survivors,k,epochs,sel,evghosts):
    worlds,pacmen,ghosts = initialize(popsize,mdepth,lsize,tprob,nworlds,xdim,ydim,wden,ppill)
    bestruns = []
    allruns = []
    pacid= ghostid = popsize
    for i in range(epochs):
        run = []
        print('Epoch: ' + str(i+1))
        if os.path.exists('worldfiles/epoch'+str(i+1)+'/') and os.path.isdir('worldfiles/epoch'+str(i)+'/'):
            shutil.rmtree('worldfiles/epoch'+str(i+1)+'/')
        run_epoch(i,worlds,popsize, pacmen, ghosts,nghosts,fprob,gtime)
        bestp = 0
        bestscore = 0
        best = ''
        pacmen = selection.truncsel(pacmen, survivors)
        for p in pacmen:
            avgscore = np.mean(p.allscores)
            run.append(avgscore)
            if avgscore > bestscore:
                bestscore = avgscore
                best = p.allscores
                bestp = p.identifier
                bestworld = p.allscores.index(max(p.allscores))
        allruns.append(run)
        print('Best Average Score: ' + str(avgscore))
        print('Player: ' + str(bestp))
        print('Best World: ' + str(bestworld+1))
        bestruns.append(best)
        pacid = generate_children(sel,pacmen,popsize,survivors,k,pacid,mdepth,lsize,tprob)
        if evghosts:
            ghosts = selection.truncsel(ghosts,survivors)
            ghostid = generate_children(sel,ghosts,popsize,survivors,k,ghostid,mdepth,lsize,tprob,xdim,ydim)
    fig = plt.figure()
    plt.violinplot(bestruns)
    plt.boxplot(bestruns)
    fig.suptitle('Best Runs from Each Epoch')
    plt.show()
    plt.clf()
    fig = plt.figure()
    plt.violinplot(allruns)
    plt.boxplot(allruns)
    fig.suptitle('Mean Scores from Each Epoch')
    plt.show()