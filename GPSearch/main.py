#Alec Bayliff
import evolution
import time
#Number of worlds
nworlds = 30
#Population size
popsize = 30
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
clim = 20
#Parents
parents = 10
epochs = 100
selection = 'fitprop'
evghosts = False

if __name__ == '__main__':
    start_time = time.time()
    evolution.run(nworlds,popsize,mdepth,lsize,tprob,xdim,ydim,wden,ppill,rnginit,nghosts,fprob,gtime,clim,parents,epochs,selection,evghosts)
    print("--- %s seconds ---" % (time.time() - start_time))