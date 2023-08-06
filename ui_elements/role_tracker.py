import tkinter as tk
import os
from PIL import ImageTk, Image

from gameplay.enums import ActionCost

class RoleTracker(object):
    def __init__(self, root, remaining_roles):
        self.canvas = tk.Canvas(root, width=500, height=80)
        self.canvas.place(x=20, y=450) 
        self.icons = create_icons(self.canvas)

    def update_role_tracker(self, remaining_roles):
        self.icons = update_icons(self.canvas, remaining_roles)        
            
    def create_role(self, role, age):
        self.canvas.create_rectangle(30, 0, 190, 20, fill='white', outline="")
        self.canvas.create_text(110, 10, text=role + " Age: " + age)
        
    def delete_role(self):
        self.canvas.create_rectangle(60, 0, 160, 20, fill='white', outline="")
        
def update_icons(canvas, remaining_roles):
    if 'Engineer' in remaining_roles:
        canvas.create_oval((50,40,70,60), fill='green')
    if 'Doctor' in remaining_roles:
        canvas.create_oval((90,40,110,60), fill='green')
    if 'Teacher' in remaining_roles:
        canvas.create_oval((130,40,150,60), fill='green')
    if 'Violent Criminal' in remaining_roles:
        canvas.create_oval((170,40,190,60), fill='green')
    if 'Farmer' in remaining_roles:
        canvas.create_oval((210,40,230,60), fill='green')
    if 'Mayor' in remaining_roles:
        canvas.create_oval((10,40,30,60), fill='green')

def create_icons(canvas):
    #circle1 = canvas.create_oval((40,40,60,60), fill='red')
    #circle1.grid(row=0, columnspan=7, column=0, sticky='W', padx=5, pady=5)
    canvas.create_oval((50,40,70,60), fill='red')
    canvas.create_oval((90,40,110,60), fill='red')
    canvas.create_oval((130,40,150,60), fill='red')
    canvas.create_oval((170,40,190,60), fill='red')
    canvas.create_oval((210,40,230,60), fill='red')
    canvas.create_oval((10,40,30,60), fill='red')
    
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'engineer.png')
    logo = ImageTk.PhotoImage(Image.open(path).resize((50, 50), Image.ANTIALIAS))
    label = tk.Label(image=logo)
    label.image = logo
    label.place(x=50, y=530)
    #CreateToolTip(label, text='engineer')
    
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'doctor.png')
    logo = ImageTk.PhotoImage(Image.open(path).resize((50, 50), Image.ANTIALIAS))
    label = tk.Label(image=logo)
    label.image = logo
    label.place(x=90, y=530)
    
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'teacher.png')
    logo = ImageTk.PhotoImage(Image.open(path).resize((50, 50), Image.ANTIALIAS))
    label = tk.Label(image=logo)
    label.image = logo
    label.place(x=130, y=530)
    
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'robber.png')
    logo = ImageTk.PhotoImage(Image.open(path).resize((50, 50), Image.ANTIALIAS))
    label = tk.Label(image=logo)
    label.image = logo
    label.place(x=170, y=530)

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'farmer.png')
    logo = ImageTk.PhotoImage(Image.open(path).resize((50, 50), Image.ANTIALIAS))
    label = tk.Label(image=logo)
    label.image = logo
    label.place(x=210, y=530)

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'mayor.png')
    logo = ImageTk.PhotoImage(Image.open(path).resize((50, 50), Image.ANTIALIAS))
    label = tk.Label(image=logo)
    label.image = logo
    label.place(x=10, y=530)

    

