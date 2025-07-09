#Alec Bayliff
from worldgen import World
from players import PacMan
from players import Ghost
import controller
import numpy as np

class Game:
    def __init__(self,w,h,wd,f,t,rng,file):
        self._width = w
        self._height = h
        self._wall_density = wd
        self._fruit_spawn = f
        self._time_mult = t
        self._rng_init = rng
        self._file_name = file
        
    def play(self):
        if isinstance(self._rng_init,int):
            np.random.seed(self._rng_init)
        play_world = World(self._width,self._height,self._wall_density)
        
        pac = PacMan(play_world)
        ghost1 = Ghost(play_world,1)
        ghost2 = Ghost(play_world,2)
        ghost3 = Ghost(play_world,3)
        pac_controller = controller.PacController(3, 2, 0)
        ghost1_controller = controller.GhostController(3,2,0,ghost1.get_sym())
        ghost2_controller = controller.GhostController(3,2,0,ghost2.get_sym())
        ghost3_controller = controller.GhostController(3,2,0,ghost3.get_sym())

        play_world.print_world()
        
        f = open(self._file_name,'w')
        f.write(str(play_world.x_dim())+'\n')
        f.write(str(play_world.y_dim())+'\n')
        f.write(pac.symbol() + ' ' + str(pac.x_pos()) + ' ' + str(pac.y_pos()) +'\n')
        f.write(str(ghost1.symbol()) + ' ' + str(ghost1.x_pos()) + ' ' + str(ghost1.y_pos())+'\n')
        f.write(str(ghost2.symbol()) + ' ' + str(ghost2.x_pos()) + ' ' + str(ghost2.y_pos())+'\n')
        f.write(str(ghost3.symbol()) + ' ' + str(ghost3.x_pos()) + ' ' + str(ghost3.y_pos())+'\n')
        
        for x in range(play_world.x_dim()):
            for y in range(play_world.y_dim()):
                if play_world.world_map[x][y] == 'p':
                    f.write('p' + ' ' + str(x) + ' ' + str(y)+'\n')
                elif play_world.world_map[x][y] == 'w':
                    f.write('w' + ' ' + str(x) + ' ' + str(y)+'\n')
        f.write('t' +' '+ str(self._time_mult-x) +' '+ str(pac.score())+'\n')
        
        for x in range(self._time_mult):
            
            if np.random.random() < self._fruit_spawn and play_world.is_fruit() == False:
                while(play_world.is_fruit() == False):
                    fruitx = np.random.randint(play_world.x_dim())
                    fruity = np.random.randint(play_world.y_dim())
                    if play_world.world_map[fruitx][fruity] != 'w' and play_world.world_map[fruitx][fruity] != 'p':
                        if fruitx != pac.x_pos() and fruity != pac.y_pos():
                            play_world.world_map[fruitx][fruity] = 'f'
                            play_world.set_fruit(True)
                            f.write('f' +' '+ str(fruitx) +' '+ str(fruity)+'\n')
            pac.move(pac_controller.evaluate(pac, [ghost1,ghost2,ghost3], play_world))
            f.write(pac.symbol() + ' ' + str(pac.x_pos()) + ' ' + str(pac.y_pos())+'\n')
            ghost1.move(ghost1_controller.evaluate(pac, [ghost1,ghost2,ghost3], play_world))
            f.write(str(ghost1.symbol()) + ' ' + str(ghost1.x_pos()) + ' ' + str(ghost1.y_pos())+'\n')
            
            if pac.x_pos() == ghost1.x_pos() and pac.y_pos() == ghost1.y_pos():
                print("GAME OVER")
                print("SCORE: ", pac.score())
                break;
            ghost2.move(ghost2_controller.evaluate(pac, [ghost1,ghost2,ghost3], play_world))
            f.write(str(ghost2.symbol()) + ' ' + str(ghost2.x_pos()) + ' ' + str(ghost2.y_pos())+'\n')
            
            if pac.x_pos() == ghost2.x_pos() and pac.y_pos() == ghost2.y_pos():
                print("GAME OVER")
                print("SCORE: ", pac.score())
                break;
            ghost3.move(ghost3_controller.evaluate(pac, [ghost1,ghost2,ghost3], play_world))
            f.write(str(ghost3.symbol()) + ' ' + str(ghost3.x_pos()) + ' ' + str(ghost3.y_pos())+'\n')
            
            if pac.x_pos() == ghost3.x_pos() and pac.y_pos() == ghost3.y_pos():
                print("GAME OVER")
                print("SCORE: ", pac.score())
                break;
            f.write('t' +' '+ str(self._time_mult-1-x) +' '+ str(pac.score())+'\n')
            
        f.write('t' +' '+ str(self._time_mult-1-x) +' '+ str(pac.score())+'\n')
        f.close()
        play_world.print_world()