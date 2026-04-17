# creates a pane that displays some stats

import tkinter as tk


def build(root, w, h, num_bins=24):
    
    canvas = tk.Canvas(root, height=h, width=w)
    p = min(w, h)*.05 # 5% padding on every side
    r = min(w,h)/2-p
    center = (int(w/2), int(h/2))
    coords = (center[0]-r, center[1]-r, center[0]+r, center[1]+r)
    
    
    
    extent =360/num_bins
    for j in [extent*i for i in range(num_bins)]:
        arc_ids.append(canvas.create_arc(coords , start=j, extent=extent, fill="grey"))
       
    #reference lines, the maximum value, and the uniform dist
    reference = canvas.create_oval(coords, width =2) 
    uniform_reference = canvas.create_oval(coords, outline="red", width=2, dash = "-")
    
    # We need a text object to display the p-val
    p_val = canvas.create_text(int(w/2), int(h/2) + r + 2*p, text="p-val: 0.0")
    
    #I'll stick the stuff we need into the canvas object
    canvas.data = {
        "center": center,
        "r": r,
        "arc_ids":arc_ids,
        "reference": reference,
        "uniform": uniform_reference,
        "m" : 1/num_bins,
        "p_val_id": p_val
    }
    
    return canvas


arc_ids = []


def update_histogram(canvas, hist, p_val = 0):
    hist /= sum(hist)
    
    data = canvas.data
    R = data["r"]
    c = data["center"]
    data["m"] = max(max(hist), data["m"]) #update max value
    m = data["m"]
    for r, arc_id in zip(hist, data["arc_ids"]):
        r *= R/m #scale the radius up!
        canvas.coords(arc_id, c[0]-r, c[1]-r, c[0]+r, c[1]+r)
    
    # update the uniform dist reference
    uniform_id = data["uniform"]
    # r= m/(R*len(hist))
    r= R/(m*len(hist))
    canvas.coords(uniform_id, c[0]-r, c[1]-r, c[0]+r, c[1]+r)
    
    #update the text for p_val
    canvas.itemconfig(data["p_val_id"], text=f"p-val: {p_val:.4f}")