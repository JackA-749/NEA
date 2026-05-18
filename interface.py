import tkinter as tk
from tkinter import ttk

def Start(*args):
    BlackHoleMass = BH_mass.get()
    print(BlackHoleMass)

root = tk.Tk()
root.title("Black Hole Sim")

mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))


# Declare the type for the required variables:
BH_mass = tk.DoubleVar()
BH_Xpos = tk.DoubleVar()
BH_Ypos = tk.DoubleVar()
Photon_num = tk.IntVar()


# Create and add the slider input for the black hole mass:
BH_mass_entry = tk.Scale(mainframe, variable=BH_mass, from_=0, to=100, tickinterval=10, resolution=0.1, orient=tk.HORIZONTAL)
BH_mass_entry.grid(column=2, row=1, sticky=(tk.W, tk.E))


tk.Button(mainframe, text="convert to variable", command=Start).grid(column=3, row=3, sticky=tk.W)

tk.Label(mainframe, text="Black hole Mass").grid(column=3, row=1, sticky=tk.W)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(2, weight=1)
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

BH_mass_entry.focus_set()
root.bind("<Return>", Start)

root.mainloop()