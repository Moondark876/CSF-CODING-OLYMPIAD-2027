import os
import cv2
import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import zxingcpp
import json
from pprint import pprint
import requests

window = TkinterDnD.Tk()
window.title("E-Fridge")
window.attributes('-topmost', True)  

def find_info_from_gtin(gtin):
    """"Will eventually find product information based on the gtin number. For now, it just returns the gtin."""
    return gtin

def scan_barcode(image_path):
    """"Returns the barcode format and code from the image at the given path."""
    img = cv2.imread(image_path)
    results = zxingcpp.read_barcode(img)
    pprint(results.text)
    output = {
            "format": results.format,
            "code": results.text
        }
    return output if output else None

def on_drop(event):
    """"Handles the dr op event from drag and dropping files onto the listbox."""
    try:
        files = window.tk.splitlist(event.data)
        valid_files = []

        for file_path in files:
            if os.path.isfile(file_path):
                valid_files.append(file_path)
            else:
                messagebox.showwarning("Invalid", f"Not a valid file: {file_path}")

        if valid_files:
            with open("dropped_files.json", "w") as f:
                json.dump(valid_files, f)
            messagebox.showinfo("Success", find_info_from_gtin(scan_barcode(valid_files[0])["code"]))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
 
# Declarations
WIDTH = 800
HEIGHT = 600 
SWIDTH = window.winfo_screenwidth()
SHEIGHT = window.winfo_screenheight()
CENTREX = (SWIDTH - WIDTH) // 2
CENTREY = (SHEIGHT - HEIGHT) // 2
window.geometry(f"{WIDTH}x{HEIGHT}+{CENTREX}+{CENTREY}")

# Top of window label
label = tk.Label(window, text="Drag and drop files here", font=("Arial", 14))
label.pack(pady=10)

# Listbox to display dropped files
listbox = tk.Listbox(window, width=70, height=10)
listbox.pack(pady=10)
listbox.drop_target_register(DND_FILES)
listbox.dnd_bind('<<Drop>>', on_drop)

window.mainloop()