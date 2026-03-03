# Creates a visual representation of a soup

import tkinter as tk
import time
import Soup

def build(w, h):
    root = tk.Tk()
    root.title("A Bowl of Soup")
    C = tk.Canvas(root, height=h, width=w)
    C.pack()
    return root, C

def initialize(canvas, soup, r=3):
    colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']
    for p in soup.particles:
        x, y = p.pos[0], p.pos[1]
        p.animation_ref = canvas.create_oval(x-r, y-r, x+r, y+r, fill=colors[p.phenotype["id"]])   

def animate(root, canvas, soup, fps=24):
    while True:
        start = time.time()
        soup.move_all()
        for p in soup.particles:
            canvas.moveto(p.animation_ref, p.pos[0], p.pos[1])
            root.update()
        elapsed = time.time() - start
        time.sleep(max(1/fps-elapsed, 0))
    

if __name__ == "__main__":
    
    w, h = 400, 400
    
    root, canvas = build(w,h)
    
    c = 5 #number of classes
    soup = Soup.Soup(w, h, 200, class_dist=[1/c for _ in range(c)])
    print("Soup Initialized")

    initialize(canvas, soup)
    print("Canvas Initialized")
   
    animate(root, canvas, soup)

    
