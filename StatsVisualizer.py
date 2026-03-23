# creates a pane that displays some stats

import tkinter as tk


def build(root, w, h, num_bins=24):
    
    canvas = tk.Canvas(root, height=h, width=w)
    p = 10
    r = min(w,h)/2
    center = (int(w/2), int(h/2))
    coords = (center[0]-r+p, center[1]-r+p, center[0]+r-p, center[1]+r-p)
    
    extent =360/num_bins
    for j in [extent*i for i in range(num_bins)]:
        arc_ids.append(canvas.create_arc(coords , start=j, extent=extent))
        

    return canvas


arc_ids = []

def init_histogram():
    pass

def update_histogram(hist):
    for i, arc_id in enumerate(arc_ids):
        radius = ...
        canvas.coords(arc_id, x0, y0, x1, y1)