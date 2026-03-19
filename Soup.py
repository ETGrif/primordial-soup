import numpy as np
from numpy.random import rand
from Particle import Particle
import pyqtree as pyqt


                
class Soup:
    
    phenotypes = []
    
    # defined width, heighth and number of randomlme generated particles
    def __init__(self, w, h, n, class_dist=[1], phenotypes=None):
        self.particles = []
        self.w = w
        self.h = h
        self.class_dist = class_dist
        self.max_perception_distance = max(w/4, h/4) # TODO this should be dynamic, but for now static
    
        
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
        self.update_q_tree()
        
        for p in self.particles:
            p.move()
    
    def populate(self, pheno, n):
        for _ in range(n):
            self.particles.append(Particle(np.random.rand()*self.w, np.random.rand()*self.h, self, pheno))
        
    # for optimizing the neighborhood search
    def update_q_tree(self):
        w, h = self.w, self.h
        q_tree_offsets = [np.array(b) for b in [[-w,-h], [-w, 0], [-w, h], [0, -h], [0, 0], [0, h], [w, -h], [w,0], [w,h]]]
        mpd = self.max_perception_distance
        self.qts = [pyqt.Index(bbox=(-mpd,-mpd,self.w+mpd, self.h+mpd)) for _ in range(len(self.class_dist))] #create a qTree for each class
        for p in self.particles:
            ci = p.phenotype["id"]
            for b in q_tree_offsets:
                pos = p.pos+b
                self.qts[ci].insert(pos, (pos[0]-1, pos[1]-1, pos[0]+1, pos[1]+1))
            #include ghosts!
        
    # returns the total number of neighbors within radius R of pos, and an array of arrays,
    # each array is the list of particles of a single class.
    def get_neighbors(self, pos, R):
        # TODO account for the wrap around of space!
        overlap = (pos[0]-R, pos[1]-R, pos[0]+R, pos[1]+R) #define search space
        neighbors = [qt.intersect(overlap) for qt in self.qts] #find the neighbors of the class
        count = sum([len(x) for x in neighbors]) #find total number of neighbors found
        return count, neighbors   

    def new_phenotype(self):
        phenotype = dict()
        phenotype["id"] = len(self.phenotypes)
        self.phenotypes.append(phenotype)
        return phenotype

    def create_random_pheno(self):
            p = self.new_phenotype()
            weightMax = 5
            strongNuclearRmax=5
            weakNuclearDmax=10
            
            
            
            
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
            
            # Strong Nuclear Force
            p.update(strong_nuclear={
                "theta": [strongNuclearRmax * rand()]
            })
            
            # Weak Nuclear Force
            # the weak nuclear foce is discriminatory, so there is a phenotype for
            # every class
            t = []
            for _ in range(len(self.class_dist)):
                r = weakNuclearDmax*rand() #this is the distance of impact
                d1 = r*rand() # deccay range width
                d2 = r-d1 # growth range width
                A = 2*weightMax*rand() - weightMax #amplitude of effect
                t.append([d1, d2, A])
            p.update(weak_nuclear={
                "theta": t
            })
            
            
            return p