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
        g_vec = t[0]*np.random.normal(0, 1, (2,)) #making it a saved value so that it could be animated
        
        # directional bias
        w = self.phenotype["bias"]["weight"]
        t = self.phenotype["bias"]["theta"]
        s, c = np.sin(t[0]), np.cos(t[0])
        R = np.array(
            [[c, -s ],
             [s, c]])
        b_vec = R@self.v
        b_vec *= w/np.linalg.norm(b_vec) #rescale! NOTE: this causes a numerical error when v is near parallel to an axis, I dont thinkt its an issue
        
        
        #Grab those neighbors!
        reactiveRadius = 20
        n_neighbors, neighbors = self.soup.get_neighbors(self.pos, reactiveRadius)
        
        
        
        # Nuclear forces (both Strong and Weak) (Discriminatory)
        R = self.phenotype["strong_nuclear"]["theta"][0]
        n_vec = np.array([0.0,0.0])
        for ci, particle_class in enumerate(neighbors):
            d1, d2, A = self.phenotype["weak_nuclear"]["theta"][ci]
            for p in particle_class:
                r = p.pos - self.pos
                mag = np.linalg.norm(r)
                
                if mag <= 1e-14: continue #to prevent div by zero
                #Strong Nuclear Force
                elif mag <= R:
                    f = -(mag-R)**2/mag # find the strong force
                    
                # weak nuclear Force
                elif mag <= R + d1: #close (decay)
                    f = A/d1*(mag - R)
                elif mag <= R + d1 + d2: #far (growth)
                    f = A/d2 * (R + d1 + d2 - mag)
                # default force
                else:
                    f = 0 
                    n_neighbors -= 1 #if the particle was out of range, dont include in the avg
                
                #apply the force
                n_vec += f*r/mag  # in direction of r
        n_vec /= n_neighbors #we want the average force        
        
        
                
        
        self.v = g_vec + b_vec + n_vec #store it for reference in next step
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
        