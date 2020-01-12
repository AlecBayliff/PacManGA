#Alec Bayliff
from worldgen import World
from players import PacMan
from players import Ghost
import numpy as np
        
test = World(15,15,42,.25)
    
pac = PacMan(test)
g = Ghost(test,1)
g1 = Ghost(test,2)
g2 = Ghost(test,3)

for line in test.world:
    print(line)

f = open('testout.txt','w')
f.write(str(test.x_dim)+'\n')
f.write(str(test.y_dim)+'\n')
f.write(pac.symbol + ' ' + str(pac.x_pos) + ' ' + str(pac.y_pos) +'\n')
f.write(str(g.symbol) + ' ' + str(g.x_pos) + ' ' + str(g.y_pos)+'\n')
f.write(str(g1.symbol) + ' ' + str(g1.x_pos) + ' ' + str(g1.y_pos)+'\n')
f.write(str(g2.symbol) + ' ' + str(g2.x_pos) + ' ' + str(g2.y_pos)+'\n')
for x in range(test.x_dim):
    for y in range(test.y_dim):
        if test.world[x][y] == 'p':
            f.write('p' + ' ' + str(x) + ' ' + str(y)+'\n')
        elif test.world[x][y] == 'w':
            f.write('w' + ' ' + str(x) + ' ' + str(y)+'\n')
f.write('t' +' '+ str(500-x) +' '+ str(pac.score)+'\n')
for x in range(500):
    pac.move()
    f.write(pac.symbol + ' ' + str(pac.x_pos) + ' ' + str(pac.y_pos)+'\n')
    g.move()
    f.write(str(g.symbol) + ' ' + str(g.x_pos) + ' ' + str(g.y_pos)+'\n')
    if pac.x_pos == g.x_pos and pac.y_pos == g.y_pos:
        print("GAME OVER")
        print("SCORE: ", pac.score)
        break;
    g1.move()
    f.write(str(g1.symbol) + ' ' + str(g1.x_pos) + ' ' + str(g1.y_pos)+'\n')
    if pac.x_pos == g1.x_pos and pac.y_pos == g1.y_pos:
        print("GAME OVER")
        print("SCORE: ", pac.score)
        break;
    g2.move()
    f.write(str(g2.symbol) + ' ' + str(g2.x_pos) + ' ' + str(g2.y_pos)+'\n')
    if pac.x_pos == g2.x_pos and pac.y_pos == g2.y_pos:
        print("GAME OVER")
        print("SCORE: ", pac.score)
        break;
    f.write('t' +' '+ str(499-x) +' '+ str(pac.score)+'\n')
f.write('t' +' '+ str(499-x) +' '+ str(pac.score)+'\n')
f.close()

for line in test.world:
    print(line)