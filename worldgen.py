#Alec Bayliff
import numpy as np

class World:
    def __init__(self,x_dim,y_dim,seed,percent):
        np.random.seed(seed)
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.percent = percent
        self.world = []
        self.generate_world()
        self.carve()
        
    def generate_world(self):
        for x in range(self.x_dim):
            plane = []
            for y in range(self.y_dim):
                plane.append('w')
            self.world.append(plane)
    
    def carve(self):
        augmented_world = self.world
        for x in range(self.x_dim):
            for y in range(self.y_dim):
                if(x >= 0 and y == 0) or (y >= 0 and x == 0):
                    augmented_world[x][y] = ' '
                elif(x <= self.x_dim and y == self.y_dim-1) or (y <= self.y_dim and x == self.x_dim-1):
                    augmented_world[x][y] = ' '
                elif(x > 0 and y > 0 and x < self.x_dim and y < self.y_dim):
                    if np.random.random() > self.percent:
                        if np.random.random() > self.percent and self.check_neighbor(augmented_world,x,y):
                            augmented_world[x][y] = 'p'
                        elif self.check_neighbor(augmented_world,x,y):
                            augmented_world[x][y] = ' '
        self.world = augmented_world
    
    def check_neighbor(self,augmented_world,x,y):
        if x < 0 or y < 0 or x > self.x_dim or y > self.y_dim:
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
