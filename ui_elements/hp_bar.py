import tkinter as tk
import os
from PIL import ImageTk, Image

class HpBar(object):
    def __init__(self, root, max_hp): #initialize hp ui
        self.canvas = tk.Canvas(root, width=max_hp/2 + 20, height=30)
        self.canvas.place(x=370, y=650)
        self.render(max_hp)
        self.max_hp = max_hp
    
    def render(self, max_hp): # render hp bar
        tk.Label(self.canvas, text="HP", font=("Arial", 18)).place(x=0, y=0)
        HpBar.create_unit(self.canvas, 20, 6, max_hp/2 + 20, max_hp/2 + 20)
        
    def update_hp(self, remaining_hp): # passes in updated hp values
        HpBar.create_unit(self.canvas, 20, 6, remaining_hp/2, self.max_hp/2 + 20)
    
    
    def create_unit(canvas, x, y, length, max_size): # creates remaining hp rectangle in red and rest of the bar in white
        return canvas.create_rectangle(x, y, x+length, y+20, fill='red') + canvas.create_rectangle(x+length, y, max_size, y+20, fill='white')