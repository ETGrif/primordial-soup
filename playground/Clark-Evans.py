import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import Soup

import numpy as np
import scipy as sp
import plotly.graph_objects as go


w, h = 400, 400
n=400



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


N = 250
dists = [single_experiment() for _ in range(N)]
mu = sum(dists)/N
sig = np.var(dists)
print(f"mean: {mu}")
print(f"variance: {sig}")

fig = go.Figure()
fig.add_histogram(x=dists, histnorm='probability density', name="E(r) dist")
fig.update_layout(title={"text":"Histogram"})
xref = np.linspace(min(dists), max(dists), 100)
yref = sp.stats.norm.pdf(xref, mu, sig)
fig.add_scatter(x=xref, y=yref, name="normal reference")
fig.show()


## QQ plot
fig = go.Figure()
ref = sp.stats.norm.rvs(mu, sig, N)
fig.add_scatter(x=sorted(ref), y=sorted(dists), name="Dist")
fig.update_layout(title={"text":"QQPlot"})
fig.add_scatter(x=[min(ref), max(ref)], y=[min(ref), max(ref)], name="reference")
fig.show()

    
            
            
    