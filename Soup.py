import numpy as np
from numpy.random import rand
from Particle import Particle


                
class Soup:
    
    phenotypes = []
    
    # defined width, heighth and number of randomlme generated particles
    def __init__(self, w, h, n, class_dist=[1], phenotypes=None):
        self.particles = []
        self.w = w
        self.h = h
        self.class_dist = class_dist
    
        
        #Populate with class_dist. If presesnt, use premade phenotypes, othewise generate randomly.
        
        assert np.isclose(sum(class_dist), 1), "Invalid Class Dist."
        if phenotypes != None: assert len(phenotypes) == len(class_dist), "Different number of phenotypes than classes."
        
        for i, C in enumerate(class_dist):
            if phenotypes==None:
                # premade not present, generate new random phenotype
                self.populate(self.create_random_pheno(), int(C*n))
            else:
                # use the premade phenotypes
                p = self.new_phenotype()
                p.update(phenotypes[i])
                self.populate(p, int(C*n))
        
            
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
                "theta": [np.pi/2 - np.pi*rand()]
            })
            
            
            return p