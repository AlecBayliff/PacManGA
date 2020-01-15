#Alec Bayliff
import numpy as np

class World:
    def __init__(self,x_dim,y_dim,wall_density):
        self._xdim = x_dim
        self._ydim = y_dim
        self._wall_density = wall_density
        self.fruit_placed = False
        self.world_map = []
        self.generate_world()
        self.carve()
        
    def generate_world(self):
        for x in range(self._xdim):
            plane = []
            for y in range(self._ydim):
                plane.append('w')
            self.world_map.append(plane)
    
    def carve(self):
        augmented_world = self.world_map
        for x in range(self._xdim):
            for y in range(self._ydim):
                if(x >= 0 and y == 0) or (y >= 0 and x == 0):
                    augmented_world[x][y] = ' '
                elif(x <= self._xdim and y == self._ydim-1) or (y <= self._ydim and x == self._xdim-1):
                    augmented_world[x][y] = ' '
                elif(x > 0 and y > 0 and x < self._xdim and y < self._ydim):
                    if np.random.random() > self._wall_density:
                        if np.random.random() > self._wall_density and self.check_neighbor(augmented_world,x,y):
                            augmented_world[x][y] = 'p'
                        elif self.check_neighbor(augmented_world,x,y):
                            augmented_world[x][y] = ' '
        self.world_map = augmented_world
    
    def check_neighbor(self,augmented_world,x,y):
        if x < 0 or y < 0 or x > self._xdim or y > self._ydim:
            print("DIM ERROR",x,y)
        else:
            if augmented_world[x-1][y] == ' ' or augmented_world[x-1][y] == 'p':
                return True
            if augmented_world[x][y-1] == ' ' or augmented_world[x][y-1] == 'p':
                return True
            if augmented_world[x+1][y] == ' ' or augmented_world[x+1][y] == 'p':
                return True
            if augmented_world[x][y+1] == ' ' or augmented_world[x][y+1] == 'p':
                return True
            return False
        
    def x_dim(self):
        return self._xdim
    
    def y_dim(self):
        return self._ydim
    
    def print_world(self):
        for line in self.world_map:
            print(line)
