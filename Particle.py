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
        
        
        
        #Strong Nuclear Force
        R = self.phenotype["nuclear"]["theta"][0]
        s_vec = np.array([0.0,0.0])
        for particle_class in neighbors:
            for p in particle_class:
                r = p.pos - self.pos
                mag = np.linalg.norm(r)
                if mag <= R:
                    f = (mag-R)**2/mag # find the strong force
                    s_vec += f*r/mag  # apply the force with mag f in the direction of r
                    
                
                
        
        self.v = g_vec + b_vec #store it for reference in next step
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
        