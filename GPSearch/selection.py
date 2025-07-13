# -*- coding: utf-8 -*-
"""
Created on Sat Jul 12 21:32:35 2025

@author: Alec
"""

import random

def ktournament(players,k,replacement=False):
    if replacement == False:
        tournament = random.sample(players,k)
    else:
        tournament = random.choices(players,k=k)
    maxscore = 0
    maxpos = 0
    for i in range(k):
        if tournament[i].score() > maxscore:
            maxscore = tournament[i].score()
            maxpos = i
    return tournament[maxpos]

def fitpropsel(players):
    scores = []
    for p in players:
        scores.append(p.score())
    return random.choices(players,weights=scores,k=2)

def truncsel(players,n):
    scores = []
    selected = []
    for p in players:
        scores.append(p.score())
    scores.sort(reverse=True)
    scores = scores[:n]
    for p in players:
        if p.score() in scores:
            selected.append(p)
    return selected