#Alec Bayliff
import numpy as np

class Game:
    #This can handle an arbitrary number of ghosts > 0, however, the vizualizer needs 3
    def __init__(self,f,t,file):
        self._fruit_spawn = f
        self._time_mult = t
        self._file_name = file
    
    def play(self,pac,ghosts,play_world):
        #Initialize the controllers
        pac.reset()
        pac.load_world(play_world)
        pac_controller = pac.controller
        ghost_win = [False for x in range(len(ghosts))]
        ghost_controllers = []
        for g in ghosts:
            g.reset(play_world.x_dim,play_world.y_dim)
            g.load_world(play_world)
            g.controller.ego = g.symbol
            ghost_controllers.append(g.controller)
        
        f = open(self._file_name,'w')
        f.write(str(play_world.x_dim)+'\n')
        f.write(str(play_world.y_dim)+'\n')
        f.write(pac.symbol + ' ' + str(pac.x_pos) + ' ' + str(pac.y_pos) +'\n')
        for g in ghosts:
            f.write(str(g.symbol) + ' ' + str(g.x_pos) + ' ' + str(g.y_pos)+'\n')
        
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
                print('PacMan wins!')
                pac.win_score(t,self._time_mult)
                break;
            
            for g in range(len(ghosts)):
                ghosts[g].move(ghost_controllers[g].evaluate(pac,ghosts,play_world))
                f.write(str(ghosts[g].symbol) + ' ' + str(ghosts[g].x_pos) + ' ' + str(ghosts[g].y_pos)+'\n')
                if pac.x_pos == ghosts[g].x_pos and pac.y_pos == ghosts[g].y_pos:
                    score = (np.log(self._time_mult) - np.log(t))
                    ghosts[g].score = score
                    ghost_win[g] = True
            
            f.write('t' +' '+ str(self._time_mult-1-t) +' '+ str(pac.score)+'\n')
            
            if True in ghost_win:
                for g in ghosts:
                    g.update_score(np.log(self._time_mult) - np.log(t))
                    g.final_score()
                break;
        f.close()
        if play_world.pills:
            pac.final_score()