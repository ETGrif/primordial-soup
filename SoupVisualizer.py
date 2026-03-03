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
    for p in soup.particles:
        x, y = p.pos[0], p.pos[1]
        p.animation_ref = canvas.create_oval(x-r, y-r, x+r, y+r, fill="black")   

def animate(root, canvas, soup, fps=24):
    while True:
        start = time.time()
        soup.move_all()
        for p in soup.particles:
            canvas.move(p.animation_ref, p.v[0], p.v[1])
            root.update()
        elapsed = time.time() - start
        time.sleep(abs(1/fps-elapsed))
    

if __name__ == "__main__":
    
    w, h = 400, 400
    
    root, canvas = build(w,h)
    
    soup = Soup.Soup(w, h, 200)

    initialize(canvas, soup)
   
    animate(root, canvas, soup)

    
