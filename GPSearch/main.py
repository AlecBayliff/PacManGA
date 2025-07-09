#Alec Bayliff
from play import Game
import numpy as np
import tree
from worldgen import World
from players import PacMan, Ghost

mygame = Game(15,15,.25,.1,1000,42,'testout.txt')
mygame.play()
