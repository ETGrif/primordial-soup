import numpy as np
from Particle import Particle


BIAS = "bias"
        
        
class Soup:
    
    # defined width, heighth and number of randomlme generated particles
    def __init__(self, w, h, n, complexity):
        self.particles = []
        self.w = w
        self.h = h
        self.complexity = complexity
        
        self.populate(create_random_pheno(), n)
        
            
    def move_all(self):
        for p in self.particles:
            p.move()
    
    def populate(self, pheno, n):
        for _ in range(n):
            self.particles.append(Particle(np.random.rand()*self.w, np.random.rand()*self.h, self, pheno))
        


def create_random_pheno():
        p = dict()
        
        # bias. Unit vector in a uniform direction
        theta = np.random.rand()*np.pi*2
        p[BIAS] = np.array([np.sin(theta), np.cos(theta)])
        
        return p