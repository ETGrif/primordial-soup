import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import SoupVisualizer as sv
import Soup

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

soup = Soup.Soup(w, h, 200, class_dist=[.5, .5], phenotypes=[p1,p2])
sv.initialize(canvas, soup, trails=True)
sv.animate(root, canvas, soup, fps=24, trail_length=30)