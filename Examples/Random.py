import sys
from pathlib import Path
#this lets us import from the root directory
sys.path.append(str(Path(__file__).parent.parent))

import SoupVisualizer as sv
import Soup


w, h = 400, 400
c = 4 #the number of classes

root, canvas = sv.build(w,h)


soup = Soup.Soup(w, h, 200, class_dist=[1/c for _ in range(c)], phenotypes=None)
sv.initialize(canvas, soup, trails=True)
sv.animate(root, canvas, soup, fps=24, trail_length=30)