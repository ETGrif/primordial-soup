import numpy as np
from numpy.random import rand
from Particle import Particle


                
class Soup:
    
    phenotypes = []
    
    # defined width, heighth and number of randomlme generated particles
    def __init__(self, w, h, n, class_dist=[1]):
        self.particles = []
        self.w = w
        self.h = h
        self.class_dist = class_dist
        
        #create C = n*class_dist agents with a common phenotype
        for C in class_dist:
            self.populate(self.create_random_pheno(), int(C*n))
        
            
    def sim_step(self):
        for p in self.particles:
            p.move()
    
    def populate(self, pheno, n):
        for _ in range(n):
            self.particles.append(Particle(np.random.rand()*self.w, np.random.rand()*self.h, self, pheno))
        
    def new_phenotype(self):
        phenotype = dict()
        phenotype["id"] = len(self.phenotypes)
        self.phenotypes.append(phenotype)
        return phenotype

    def create_random_pheno(self):
            p = self.new_phenotype()
            weightMax = 5
            
            
            #Brownian
            # [sigma]
            sigmaRange = (1,5)
            p.update(gaussian = {
                    "theta": [sigmaRange[0] + (sigmaRange[1]-sigmaRange[0])*rand()]
                }) 
            
            #directional bias
            p.update(bias= {
                "weight": weightMax * rand(),
                "theta": [2*np.pi*rand()]
            })
            
            
            return p