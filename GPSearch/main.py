#Alec Bayliff
from play import Game
from worldgen import World
from players import PacMan, Ghost

mdepth = 3
treesize = 2
prob = .1
play_world = World(15,15,.25)
pacman = PacMan(mdepth,treesize,prob,play_world)
ghosts = [Ghost(mdepth,treesize,prob,play_world,g+1) for g in range(3)]

mygame = Game(.1,1000,42,'testout.txt',3)
mygame.play(pacman,ghosts,play_world)
print('PacScore:')
print(pacman.score())
print('GhostScores:')
for g in ghosts:
    print(g.score())
