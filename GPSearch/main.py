#Alec Bayliff
import evolution
#Number of worlds
nworlds = 5
#Population size
popsize = 10
#Max initial tree depth
mdepth = 3
#Number of leaves allowed
lsize = 3
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
clim = 5
#Parents
parents = 4
epochs = 10
selection = 'fitprop'
evghosts = True

if __name__ == '__main__':
    evolution.run(nworlds,popsize,mdepth,lsize,tprob,xdim,ydim,wden,ppill,rnginit,nghosts,fprob,gtime,clim,parents,epochs,selection,evghosts)