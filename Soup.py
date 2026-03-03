import numpy as np
from Particle import Particle


BIAS = "bias"
ID = "id"

                
class Soup:
    
    pheno_id_count = 0
    
    # defined width, heighth and number of randomlme generated particles
    def __init__(self, w, h, n, class_dist=[1]):
        self.particles = []
        self.w = w
        self.h = h
        self.class_dist = class_dist
        
        #create C = n*class_dist agents with a common phenotype
        for C in class_dist:
            self.populate(self.create_random_pheno(), int(C*n))
        
            
    def move_all(self):
        for p in self.particles:
            p.move()
    
    def populate(self, pheno, n):
        for _ in range(n):
            self.particles.append(Particle(np.random.rand()*self.w, np.random.rand()*self.h, self, pheno))
        

    def create_random_pheno(self):
            p = dict()
            
            #pheno id
            p[ID] = self.pheno_id_count
            self.pheno_id_count += 1 #increment!
            
            # bias. Unit vector in a uniform direction
            theta = np.random.rand()*np.pi*2
            p[BIAS] = np.array([np.sin(theta), np.cos(theta)])
            
            return p