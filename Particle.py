import numpy as np

"""
A Particle takes in 
"""
class Particle:
    def __init__(self, x, y, soup, phenotype):
        self.pos = np.array([x,y])
        self.v = np.array([0,0]) #just to initialize
        
        self.soup = soup
        self.phenotype = phenotype
        
        
    def move(self):
        #This function needs to make an update based on the X = n + g + b rules
        self.v = np.random.normal(0, 1, (2,)) #making it a saved value so that it could be animated
        self.v += self.phenotype["bias"]
        self.pos += self.v
        
        #wrap around!
        h = self.soup.h
        w = self.soup.w
        x = self.pos[0]
        y = self.pos[1]
        
        if x < 0: x += w
        if y < 0: y += h
        if x >= w: x-= w
        if y >= h: y-= h
        self.pos = np.array([x,y])
        