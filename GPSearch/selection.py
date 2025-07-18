# -*- coding: utf-8 -*-
"""
Created on Sat Jul 12 21:32:35 2025

@author: Alec
"""

import random
import numpy as np

#Might add reward-based selection. Players can be updated with Player.update_score()
#But keeping track of children and grandchildren would require some changes.

def ktournament(players,k,parents,replacement=False):
    results = []
    for i in range(parents):
        if replacement == False:
            tournament = random.sample(players,k)
        else:
            tournament = random.choices(players,k=k)
        maxscore = 0
        maxpos = 0
        for i in range(k):
            avgscore = np.mean(tournament[i].allscores)
            if avgscore > maxscore:
                maxscore = avgscore
                maxpos = i
        results.append(tournament[maxpos])
    return results

def fitpropsel(players,parents):
    scores = []
    for p in players:
        scores.append(np.mean(p.allscores))
    return random.choices(players,weights=scores,k=parents)

def truncsel(players,n):
    scores = []
    selected = []
    for p in players:
        scores.append(np.mean(p.allscores))
    scores.sort(reverse=True)
    scores = scores[:n]
    for p in players:
        avgscore = np.mean(p.allscores)
        if avgscore in scores:
            selected.append(p)
    return selected