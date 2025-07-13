#Alec Bayliff
from play import Game
import numpy as np
import tree
from worldgen import World
from players import PacMan, Ghost


play_world = World(15,15,.25)
pacman = PacMan(play_world)
ghosts = [Ghost(play_world,g+1) for g in range(3)]

mygame = Game(.1,1000,42,'testout.txt',3)
mygame.play(pacman,ghosts,play_world)
print('PacScore:')
print(pacman.score())
print('GhostScores:')
for g in ghosts:
    print(g.score())
