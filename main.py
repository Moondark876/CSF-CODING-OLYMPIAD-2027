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
    """"Finds product information based on the gtin number."""
    response = requests.get(f"https://world.openfoodfacts.net/api/v2/product/{gtin}?fields=product_name,brands,ingredients_text,expiration_date,front")
    if response.status_code == 200:
        return response.json()
    else:
        messagebox.showerror("Error", f"Failed to fetch product information for GTIN {gtin}. Status code: {response.status_code}")
        return 

def scan_barcode(image_path):
    """"Returns the GTIN from the image at the given path."""
    img = cv2.imread(image_path)
    results = zxingcpp.read_barcode(img)
    if results:
        return results.text

def on_drop(event):
    """"Handles the drop event from drag and dropping files onto the listbox."""
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
            for file in valid_files:
                code = scan_barcode(file)
                if not code:
                    messagebox.showerror("Error", (len(valid_files) > 1 and "["+str(valid_files.index(file)+1)+"] " or "") + "No barcode found in the image.")
                    continue
                info = find_info_from_gtin(code)
                if info:
                    pprint(info)
                    messagebox.showinfo("Success", info["product"]["product_name"] + " has been found and added to your fridge!")
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