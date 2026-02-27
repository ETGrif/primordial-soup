import numpy as np

"""
A Particle takes in 
"""
class Particle:
    def __init__(self, x, y):
        self.pos = np.array([x,y])
        self.v = np.array([0,0]) #just to initialize
        
        
    def move(self):
        #This function needs to make an update based on the X = n + g + b rules
        # TODO Right now I just want it to move left
        self.v = np.random.normal(0, 1, (2,)) #making it a saved value so that it could be animated
        self.pos += self.v
        
        
class Soup:
    
    # defined width, heighth and number of randomlme generated particles
    def __init__(self, w, h, n):
        self.particles = []
        for _ in range(n):
            self.particles.append(Particle(np.random.rand()*w, np.random.rand()*h))
            
    def move_all(self):
        for p in self.particles:
            p.move()
        
        
        
        
    