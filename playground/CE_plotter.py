import pickle as pk
import numpy as np
import scipy as sp

import plotly.graph_objects as go

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import ClarkEvansUtil as ce

dump_file = 'CE Experiment Dump.txt'

with open(dump_file, "rb") as fin:
    data = fin.readlines()
    data = [float(d) for d in data]
    print(f"{len(data)} datums found.")
    
    
    mu = np.mean(data)
    sig = np.var(data)
    sqsig=np.sqrt(sig)
    
    data = [(d-mu)/sqsig for d in data]
    
    print(f"Mu: {mu}")
    print(f"Sigma: {sig}")
    
    fig = go.Figure()
    fig.add_histogram(x=data, histnorm='probability density', name="E(r) dist")
    fig.update_layout(title={"text":"Histogram"})
    xref = np.linspace(min(data), max(data), 100)
    yref = sp.stats.norm.pdf(xref, 0, 1)
    fig.add_scatter(x=xref, y=yref, name="normal reference")
    fig.show()
    
    ce.store_new_data((mu, sig), 400, 400, 200)
    
    
    
    
    