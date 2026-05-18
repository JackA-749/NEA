import tkinter as tk
from tkinter import ttk

def Start(*args):
    BlackHoleMass = BH_mass.get()
    BlackHoleX = BH_Xpos.get()
    BlackHoleY = BH_Ypos.get()
    print(f"Mass={BlackHoleMass}, X={BlackHoleX}, Y={BlackHoleY}")

def LoadInfo(*args):
    # When the User clicks the information button, this function will open a new window with the information about the program and how to use it.
    pass

root = tk.Tk()
root.title("Black Hole Sim")
root.geometry("960x540")

mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))


# Declare the type for the required variables:
BH_mass = tk.DoubleVar()
BH_Xpos = tk.DoubleVar()
BH_Ypos = tk.DoubleVar()
Photon_num = tk.IntVar()

# Create Program Title label:
Program_title = tk.Label(mainframe, text="Black Hole Simulator", font=("Arial", 24))
Program_title.grid(column=1, row=0, columnspan=4, sticky=(tk.W, tk.E)) # have title span across all columns so it is centered


# Create and add the slider input and title for the black hole mass:
tk.Label(mainframe, text="Black hole Mass", font=("Arial", 12)).grid(column=1, row=1, columnspan=4, sticky=(tk.W, tk.E))
BH_mass_entry = tk.Scale(mainframe, variable=BH_mass, from_=0, to=100, tickinterval=10, resolution=0.05, orient=tk.HORIZONTAL)
BH_mass_entry.grid(column=1, row=2, columnspan=4, sticky=(tk.W, tk.E))

# Create and add the inputs and titles for the black hole position:
tk.Label(mainframe, text="Black hole X position", font=("Arial", 12)).grid(column=1, row=3, columnspan=2, sticky=(tk.W, tk.E))
BH_Xpos_entry = tk.Entry(mainframe, textvariable=BH_Xpos)
BH_Xpos_entry.grid(column=1, row=4, columnspan=2, sticky=(tk.W, tk.E))

tk.Label(mainframe, text="Black hole Y position", font=("Arial", 12)).grid(column=3, row=3, columnspan=2, sticky=(tk.W, tk.E))
BH_Ypos_entry = tk.Entry(mainframe, textvariable=BH_Ypos)
BH_Ypos_entry.grid(column=3, row=4, columnspan=2, sticky=(tk.W, tk.E))


tk.Button(mainframe, text="convert to variable", command=Start).grid(column=4, row=20, sticky=tk.W)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Give each column in the mainframe a weight so columnspan centering works
mainframe.columnconfigure(1, weight=1)
mainframe.columnconfigure(2, weight=1)
mainframe.columnconfigure(3, weight=1)
mainframe.columnconfigure(4, weight=1)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

BH_mass_entry.focus_set()
root.bind("<Return>", Start)

root.mainloop()