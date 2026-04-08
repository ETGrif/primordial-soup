import Soup
import pickle
import numpy as np
import scipy as sp
import os

pickle_path = "CE-ECDF_data.pkl"

def single_experiment():
    # generate a soup
    soup = Soup.Soup(w,h,n)
    soup.update_q_tree()
    
    def find_nearest(p, search_dist=50):
        neighbors = soup.get_neighbors(p.pos, search_dist) #only take the top one
        
        #increase search area if needed
        if len(neighbors) == 0:
            return find_nearest(p, search_dist*2)
        
        dists = [np.linalg.norm(p.pos - pn) for pn in neighbors]
        return min(dists)
    
    dists = [find_nearest(p) for p in soup.particles]
    return sum(dists)/len(dists)

class ClarkEvensUtil:
    def __init__(self, w, h, n):
        self.path = pickle_path
        self.args = (w, h, n)
        self.load_data() #loads the file and stores the correct data
        
        

    def load_pickle(self):
        try:
            with open(self.path, "rb") as fin:
                data = pickle.load(fin)
        except FileNotFoundError:
            print(f"ClarkEvans file, {self.path}, not found")
        
        if not isinstance(data, dict):
            raise TypeError("ClarkEvans Pickle file must contain a dictionary.")
        
        return data
        
    def load_data(self):
        pk_data = self.load_pickle() 
        #we will reread this file each time it loads so that it doesnt store unneccesarry data
        
        if self.args not in pk_data:
            raise KeyError(f"No ECDF data found for parameters: {self.args}")
        
        self.data = pk_data[self.args]
        
        if not isinstance(self.data, list):
            raise TypeError(f"ECDF not stored as a list. {type(self.data)}")
       
    def pval(self, observed):
        frac_below = np.searchsorted(self.data, observed, side='right') / len(self.data)
        return 2 * min(frac_below, 1 - frac_below) 
        
def store_new_data(data, w, h, n):
    args = (w, h, n)
    
    # read fil if exists, create one otherwise
    if os.path.exists(pickle_path):
        with open(pickle_path, "rb") as fin:
            all_data = pickle.load(fin)
    else:
        all_data = dict()
        
    # update the dataset
    all_data[args] = data
    
    #write the data!
    with open(pickle_path, "wb") as fout:
        pickle.dump(all_data, fout)
  
    
    
        
    
    
