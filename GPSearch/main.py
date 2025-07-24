#Alec Bayliff
import evolution
import time
#Number of worlds
nworlds = 30
#Population size
popsize = 50
#Max initial tree depth
mdepth = 5
#Number of branches
bsize = 2
#Tree generation probability
tprob = .05
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
#Survivor limit
survivors = 15
#K for k tournament
k = 5
epochs = 100
selection = 'fitprop'
evghosts = True

if __name__ == '__main__':
    start_time = time.time()
    evolution.run(nworlds,popsize,mdepth,bsize,tprob,xdim,ydim,wden,ppill,rnginit,nghosts,fprob,gtime,survivors,k,epochs,selection,evghosts)
    print("--- %s seconds ---" % (time.time() - start_time))