#Alec Bayliff
import numpy as np
import random

class World:
    def __init__(self,x_dim,y_dim,pwall,ppill):
        self._xdim = x_dim
        self._ydim = y_dim
        self._pwall = pwall
        self._ppill = ppill
        self._fruit = []
        self._pills = []
        self._resetpills = []
        self._world_map = []
        self.generate_world()
        
    def generate_world(self):
        visited = []
        for x in range(self._xdim):
            plane = []
            v = []
            for y in range(self._ydim):
                plane.append('w')
                v.append(False)
            visited.append(v)
            self._world_map.append(plane)
        self._world_map[0][0] = ' '
        self._world_map[self._xdim-1][self._ydim-1] = ' '
        if random.getrandbits(1):
            self._world_map[self._xdim-2][self._ydim-1] = ' '
        else:
            self._world_map[self._xdim-1][self._ydim-2] = ' '
        self.carve(0,0,visited)
        self.remove_walls()
    
    def carve(self,x,y,visited):
        visited[x][y] = True
        neighbors = [(x-2,y),(x+2,y),(x,y-2),(x,y+2)]
        random.shuffle(neighbors)
        for (nx,ny) in neighbors:
            if (0 <= nx < self._xdim) and (0 <= ny < self._ydim):
                if not visited[nx][ny]:
                    if x == nx and y > ny:
                        if np.random.rand() <= self._ppill:
                            self.add_pill(nx,y-1)
                            self._world_map[nx][y-1] = 'p'
                        else:
                            self._world_map[nx][y-1] = ' '
                    elif x == nx and y < ny:
                        if np.random.rand() <= self._ppill:
                            self.add_pill(nx,y+1)
                            self._world_map[nx][y+1] = 'p'
                        else:
                            self._world_map[nx][y+1] = ' '
                    elif x > nx and y == ny:
                        if np.random.rand() <= self._ppill:
                            self.add_pill(x-1,ny)
                            self._world_map[x-1][ny] = 'p'
                        else:
                            self._world_map[x-1][ny] = ' '
                    else:
                        if np.random.rand() <= self._ppill:
                            self.add_pill(x+1,ny)
                            self._world_map[x+1][ny] = 'p'
                        else:
                            self._world_map[x+1][ny] = ' '
                    if np.random.rand() <= self._ppill:
                        self.add_pill(nx,ny)
                        self._world_map[nx][ny] = 'p'
                    else:
                        self._world_map[nx][ny] = ' '
                    self.carve(nx,ny,visited)
                    
    def remove_walls(self):
        wallcount = 0
        total = 0
        for x in range(self._xdim):
            for y in range(self._ydim):
                if self._world_map[x][y] == 'w':
                    wallcount += 1
                total += 1
        walld = wallcount / total
        while walld > self._pwall:
            x = np.random.randint(0,self._xdim)
            y = np.random.randint(0,self._ydim)
            if self._world_map[x][y] == 'w':
                if np.random.rand() <= self._ppill:
                    self.add_pill(x, y)
                    self._world_map[x][y] = 'p'
                else:
                    self._world_map[x][y] = ' '
                wallcount -= 1
                walld = wallcount / total
            
    def x_dim(self):
        return self._xdim
    
    def y_dim(self):
        return self._ydim
    
    def count_walls(self,x,y):
        count = 0
        if x == 0:
            count += 1
        elif self._world_map[x-1][y] == 'w':
            count += 1
        if x == self._xdim-1:
            count += 1
        elif self._world_map[x+1][y] == 'w':
            count += 1
        if y == 0:
            count += 1
        elif self._world_map[x][y-1] == 'w':
            count += 1
        if y == self._ydim-1:
            count += 1
        elif self._world_map[x][y+1] == 'w':
            count += 1
        return count
        
    
    def add_fruit(self,x,y):
        self._fruit = [x,y]
        
    def remove_fruit(self):
        self._fruit = []
    
    def fruit(self):
        return self._fruit
    
    def add_pill(self,x,y):
        self._pills.append([x,y])
        self._resetpills.append([x,y])
        
    def remove_pill(self,x,y):
        self._pills.remove([x,y])
        
    def pills(self):
        return self._pills
    
    def world_map(self):
        return self._world_map
    
    def print_world(self):
        for line in self._world_map:
            print(line)
    
    def reset_pills(self):
        self._pills = self._resetpills.copy()