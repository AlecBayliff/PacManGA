# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 02:26:43 2025

@author: Alec
"""
from worldgen import World
from players import PacMan, Ghost

def generate_worlds(nworlds,xdim,ydim,walld,ppill):
    worlds = []
    for w in range(nworlds):
        worlds.append(World(xdim,ydim,walld,ppill))
    return worlds

def generate_pacmen(popsize,mdepth,treesize,prob):
    pacmen = []
    for p in range(popsize):
        pacmen.append(PacMan(mdepth,treesize,prob,play_world))
    return pacmen