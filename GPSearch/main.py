#Alec Bayliff
import evolution
'''
mdepth = 3
treesize = 2
prob = .1
xdim = 15
ydim = 15
play_world = World(xdim,ydim,.25,.75)
pacman = PacMan(mdepth,treesize,prob)
ghosts = [Ghost(mdepth,treesize,prob,g+1,xdim,ydim) for g in range(3)]

mygame = Game(.1,1000,'testout.txt',3)
mygame.play(pacman,ghosts,play_world)

    
play_world.print_world()
'''
worlds,pacmen,ghosts = evolution.initialize(30, 3, 2, .1, 30, 15, 15, .25, .75)
evolution.run_epoch(worlds, 30, pacmen, ghosts, 3, .1, 1000)