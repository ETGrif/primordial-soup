import numpy as np
from Particle import Particle
        
        
class Soup:
    
    # defined width, heighth and number of randomlme generated particles
    def __init__(self, w, h, n):
        self.particles = []
        self.w = w
        self.h = h
        pheno = dict(bias = np.array([1,2]))
        for _ in range(n):
            self.particles.append(Particle(np.random.rand()*w, np.random.rand()*h, self, pheno))
            
    def move_all(self):
        for p in self.particles:
            p.move()
        
        
        
        
    