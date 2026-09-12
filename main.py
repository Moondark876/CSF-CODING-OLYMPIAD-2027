import os
import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import json

window = TkinterDnD.Tk()
window.title("E-Fridge")
window.attributes('-topmost', True)  

 
# Declarations
WIDTH = 800
HEIGHT = 600 
SWIDTH = window.winfo_screenwidth()
SHEIGHT = window.winfo_screenheight()
CENTREX = (SWIDTH - WIDTH) // 2
CENTREY = (SHEIGHT - HEIGHT) // 2
window.geometry(f"{WIDTH}x{HEIGHT}+{CENTREX}+{CENTREY}")

window.mainloop()