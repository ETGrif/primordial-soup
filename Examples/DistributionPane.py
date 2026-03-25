import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import SoupVisualizer as sv
import StatsVisualizer as stat
import Soup
import tkinter as tk
import numpy as np

w, h = 400, 400

root, canvas = sv.build(w,h)

p1 = {
"gaussian":{
    "theta": [0.05]
},
"bias":{
    "weight": 0,
    "theta": [0]
},
"strong_nuclear":{
    "theta": [3]
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


N = 32

soup = Soup.Soup(w, h, 200, class_dist=[.5, .5], phenotypes=[p1,p2])

root.grid(1, 2, w, h)
canvas.grid(row=0, column=0)

C = stat.build(root, w/2, h, num_bins=N)
C.grid(row=0, column=1)

sv.initialize(canvas, soup, trails=True)

hist = np.ones(N) + np.sin(np.linspace(0, np.pi, N))*.5
hist /= sum(hist)
stat.update_histogram(C, hist)

sv.animate(root, canvas, soup, fps=24, trail_length=30)