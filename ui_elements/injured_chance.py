import tkinter as tk
import random
import os
from PIL import ImageTk, Image

from gameplay.enums import ActionCost

class InjuredChance(object):
    def __init__(self, humanoid, root):
        self.canvas = tk.Canvas(root, width=500, height=80)
        self.canvas.place(x=20, y=600)    
        self.canvas.create_text(100, 12, text= "Chance to convert to infected:", fill="black") 
        self.canvas.create_rectangle(200, 3 , 259, 20, fill = "white")
        percentage = str(round(humanoid.convert_chance * 100, 2)) + "%"
        self.canvas.create_text(230, 12, text=percentage, fill="black") 

    def update(self, humanoid):
        self.canvas.create_rectangle(200, 3 , 259, 20, fill = "white")
        percentage = str(round(humanoid.convert_chance * 100, 2)) + "%"
        self.canvas.create_text(230, 12, text=percentage, fill="black") 

    def convert(self, humanoid):
        if humanoid.state == "injured":
            rand = random.randrange(0, 100)
            if rand <= humanoid.convert_chance * 100:
                print("CONVERTED!")
                humanoid.state = "zombie"
            else:
                humanoid.did_not_convert = True
    
    def convertHypothetical(self, humanoid): #Check if the humanoid will convert HYPOTHETICALLY
        if humanoid.state == "injured":
            rand = random.randrange(0, 100)
            if not rand <= humanoid.convert_chance * 100:
                humanoid.did_not_convert = True