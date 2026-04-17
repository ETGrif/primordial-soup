import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import Soup
import ClarkEvansUtil as ce_util

import numpy as np
import scipy as sp
import plotly.graph_objects as go

import time


w, h = 400, 400
n=200


def single_experiment():
    # generate a soup
    soup = Soup.Soup(w,h,n)
    soup.update_q_tree()
    
    def find_nearest(p, search_dist=50):
        neighbors = soup.get_neighbors(p.pos, search_dist)[1][0] #only take the top one (only one class)
        
        #increase search area if needed
        if len(neighbors) == 1: #if it was 1, the only particle in search area was itself
            return find_nearest(p, search_dist*2)
        
        dists = [np.linalg.norm(p.pos - pn) for pn in neighbors if not np.allclose(p.pos, pn)]
        return min(dists)
    
    dists = [find_nearest(p) for p in soup.particles]
    return sum(dists)/len(dists)


# unill the specified time, or number, run experiments!
N_max = 50000
save_resolution = 100
max_hr = 23 #8AM


# first, open a dump_file
dump_file = "CE Experiment Dump.txt"
with open(dump_file, "+at") as file:
    
    i = 0
    while True:
        i += save_resolution
        
        
        #check stopping conditions
        if i > N_max: 
            print("Completed all experiments.")
            break
        if time.localtime().tm_hour >= max_hr:
            print("Ran out of time.")
            break
        
        # run experiment save_resolution times
        values = [single_experiment() for _ in range(save_resolution)]
            
        #dump
        lines = [str(v) + "\n" for v in values]
        file.writelines(lines)
        
        cur_time = time.localtime()
        print(f"Dump {int(i/save_resolution)} @ {cur_time.tm_hour}:{cur_time.tm_min}")
        
        
    print("Ended experiments.")
    
   


    
            
            
    