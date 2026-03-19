# Creates a visual representation of a soup

import tkinter as tk
import numpy as np
import time
import Soup


def build(w, h):
    root = tk.Tk()
    root.title("A Bowl of Soup")
    C = tk.Canvas(root, height=h, width=w)
    C.pack()
    return root, C

def initialize(canvas, soup, r=3, trails=False):
    colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']
    for p in soup.particles:
        x, y, cid = p.pos[0], p.pos[1], p.phenotype["id"]
        p.animation_ref = canvas.create_oval(x-r, y-r, x+r, y+r, fill=colors[cid])
        
        # trails
        if trails:
            p.history=[x, y]*2
            p.trail_ref = canvas.create_line(p.history, fill=colors[cid])
        
def animate(root, canvas, soup, fps=24, trail_length=None):
    while True:
        start = time.time()
        soup.sim_step()
        for p in soup.particles:
            # particle position
            canvas.moveto(p.animation_ref, p.pos[0], p.pos[1])
            
            # trails
            if trail_length:
                if p.wrapped_this_frame:
                    p.history = [p.pos[0], p.pos[1]]
                p.history.extend(p.pos) #add on new coords
                canvas.coords(p.trail_ref, p.history)
                
                #purge the end of the trail
                if len(p.history) >trail_length:
                    p.history.pop(0) #remove old coords
                    p.history.pop(0)
            
            root.update()
        elapsed = time.time() - start
        time.sleep(max(1/fps-elapsed, 0))
    

if __name__ == "__main__":
    
    w, h = 400, 400
    c = 2 #the number of classes
    
    root, canvas = build(w,h)
    
    p1 = {
    "gaussian":{
        "theta": [0.05]
    },
    "bias":{
        "weight": 0,
        "theta": [0]
    },
    "strong_nuclear":{
        "theta": [5]
    },
    "weak_nuclear":{
        "theta": [[3,3,2],[3,3,-6]]
    }
    }
    
    p2 = {
    "gaussian":{
        "theta": [0.05]
    },
    "bias":{
        "weight": 0,
        "theta": [0]
    },
    "strong_nuclear":{
        "theta": [5]
    },
    "weak_nuclear":{
        "theta": [[3,8,5], [3,3,2]]
    }}

    
    soup = Soup.Soup(w, h, 200, class_dist=[1/c for _ in range(c)], phenotypes=[p1, p2])
    print("Soup Initialized")

    initialize(canvas, soup, trails=True)
    print("Canvas Initialized")
   
    animate(root, canvas, soup, fps=24, trail_length=30)

    
