#Alec Bayliff
import evolution
#Number of worlds
nworlds = 3
#Population size
popsize = 15
#Max initial tree depth
mdepth = 3
#Number of leaves allowed
lsize = 2
#Tree generation probability
tprob = .1
#World x Dimension
xdim = 15
#World y Dimension
ydim = 15
#Wall density
wden = .25
#Pill probability
ppill = .75
#To seed or not
rnginit = False
#Number of ghosts
nghosts = 3
#Fruit prob each step
fprob = .1
#Game time limit
gtime = 1000
#Cull limit
clim = 10
#Parents
parents = 5
epochs = 5
selection = 'fitprop'

evolution.run(nworlds,popsize,mdepth,lsize,tprob,xdim,ydim,wden,ppill,rnginit,nghosts,fprob,gtime,clim,parents,epochs,selection)