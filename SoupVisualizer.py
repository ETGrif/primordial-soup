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
        p.r = p.phenotype["strong_nuclear"]["theta"][0]
        p.animation_ref = canvas.create_oval(x-p.r, y-p.r, x+p.r, y+p.r, fill=colors[cid])
        
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
            canvas.moveto(p.animation_ref, p.pos[0]-p.r, p.pos[1]-p.r)
            
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

    
