#Alec Bayliff
import numpy as np

class Game:
    #This can handle an arbitrary number of ghosts > 0, however, the vizualizer needs 3
    def __init__(self,f,t,file,nghosts):
        self._fruit_spawn = f
        self._time_mult = t
        self._file_name = file
        self._nghosts = nghosts
    
    def play(self,pac,ghosts,play_world):
        #Initialize the controllers
        pac.reset()
        pac.load_world(play_world)
        pac_controller = pac.controller
        ghost_win = [False for x in range(self._nghosts)]
        ghost_controllers = []
        for g in range(self._nghosts):
            ghosts[g].reset(play_world.x_dim,play_world.y_dim)
            ghosts[g].load_world(play_world)
            ghosts[g].controller.set_ego(ghosts[g].symbol)
            ghost_controllers.append(ghosts[g].controller)
        
        f = open(self._file_name,'w')
        f.write(str(play_world.x_dim)+'\n')
        f.write(str(play_world.y_dim)+'\n')
        f.write(pac.symbol + ' ' + str(pac.x_pos) + ' ' + str(pac.y_pos) +'\n')
        for g in range(self._nghosts):
            f.write(str(ghosts[g].symbol) + ' ' + str(ghosts[g].x_pos) + ' ' + str(ghosts[g].y_pos)+'\n')
        
        for x in range(play_world.x_dim):
            for y in range(play_world.y_dim):
                if play_world.world_map[x][y] == 'p':
                    f.write('p' + ' ' + str(x) + ' ' + str(y)+'\n')
                elif play_world.world_map[x][y] == 'w':
                    f.write('w' + ' ' + str(x) + ' ' + str(y)+'\n')
        f.write('t' +' '+ str(self._time_mult) +' '+ str(pac.score)+'\n')
        
        fruit_spawned = False
        for t in range(self._time_mult):
            if np.random.random() < self._fruit_spawn:
                while(not fruit_spawned):
                    fruitx = np.random.randint(play_world.x_dim)
                    fruity = np.random.randint(play_world.y_dim)
                    if play_world.world_map[fruitx][fruity] != 'w' and play_world.world_map[fruitx][fruity] != 'p':
                        if fruitx != pac.x_pos and fruity != pac.y_pos:
                            play_world.world_map[fruitx][fruity] = 'f'
                            play_world.add_fruit(fruitx,fruity)
                            f.write('f' +' '+ str(fruitx) +' '+ str(fruity)+'\n')
                            fruit_spawned = True
            pac.move(pac_controller.evaluate(pac, ghosts, play_world))
            f.write(pac.symbol + ' ' + str(pac.x_pos) + ' ' + str(pac.y_pos)+'\n')
            if not play_world.pills:
                pac.win_score(t,self._time_mult)
                break;
            
            for g in range(self._nghosts):
                ghosts[g].move(ghost_controllers[g].evaluate(pac,ghosts,play_world))
                f.write(str(ghosts[g].symbol) + ' ' + str(ghosts[g].x_pos) + ' ' + str(ghosts[g].y_pos)+'\n')
                    
                if pac.x_pos == ghosts[g].x_pos and pac.y_pos == ghosts[g].y_pos:
                    score = (self._time_mult - t)
                    ghosts[g].score = score
                    ghost_win[g] = True
            
            f.write('t' +' '+ str(self._time_mult-1-t) +' '+ str(pac.score)+'\n')
            
            if True in ghost_win:
                for g in range(self._nghosts):
                    ghosts[g].update_score(t/np.log(self._time_mult))
                    ghosts[g].final_score()
                pac.final_score()
                break;
        f.close()