# Creates a visual representation of a soup

import tkinter as tk
import numpy as np
import time
import Soup
import StatsVisualizer as sv


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
            p.trail_ref = canvas.create_line(list(p.history), fill=colors[cid])
        
def animate(root, canvas, soup, fps=24, trail_length=None, stat_pane=None, stat_sec=1):
    frame = 0
    update_stat = fps*stat_sec
    if stat_pane is not None: n_bins = len(stat_pane.data["arc_ids"])
    
    while True:
        start = time.time()
        frame += 1
        
        soup.sim_step()
        
        
        for p in soup.particles:
            # particle position
            canvas.moveto(p.animation_ref, p.pos[0]-p.r, p.pos[1]-p.r)
            
            # trails
            if trail_length:
                canvas.coords(p.trail_ref, list(p.history))
            
        if  stat_pane is not None and frame%update_stat == 0:
            sv.update_histogram(stat_pane, soup.get_directions(n_bins))
        
        root.update()
        elapsed = time.time() - start
        time.sleep(max(1/fps-elapsed, 0))

    
