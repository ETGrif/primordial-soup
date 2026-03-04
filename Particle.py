import numpy as np

"""
A Particle takes in 
"""
class Particle:
    def __init__(self, x, y, soup, phenotype):
        self.pos = np.array([x,y])
        self.v = np.array([1,0]) #just to initialize. NOT ZERO for inverse norm reasons
        
        self.soup = soup
        self.phenotype = phenotype
        
        
    def move(self):
        #This function needs to make an update based on the X = n + g + b rules
        
        # Brownian motion
        t = self.phenotype["gaussian"]["theta"]
        g_vec = np.random.normal(0, t[0], (2,)) #making it a saved value so that it could be animated
        
        # directional bias
        w = self.phenotype["bias"]["weight"]
        t = self.phenotype["bias"]["theta"]
        s, c = np.sin(t[0]), np.cos(t[0])
        R = np.array(
            [[s, c ],
             [c, -c]])
        b_vec = R@self.v
        b_vec *= t[0]/np.linalg.norm(b_vec) #rescale!
        
        
        self.v = g_vec + b_vec
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
        