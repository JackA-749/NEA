import tkinter as tk
from tkinter import ttk
from math import floor
import Simulation

def Start(*args):
    BlackHoleMass = BH_mass.get()
    BlackHoleX = BH_Xpos.get()
    BlackHoleY = BH_Ypos.get()
    photon_number = Photon_num.get()
    dt = step_size.get()
    num_steps = step_count.get()
    if num_steps == 0:
        num_steps = floor(10/dt)
    Simulation.run_simulation(BlackHoleMass, BlackHoleX, BlackHoleY, photon_number, dt, num_steps)

def LoadInfo(*args):
    # When the User clicks the information button, this function will open a new window with the information about the program and how to use it.
    Info_window = tk.Toplevel(master=root)
    Info_window.title("Info Window")
    Info_window.geometry("720x810")


root = tk.Tk()
root.title("Black Hole Sim")
root.geometry("960x900")

mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))


# Declare the type for the required variables:
BH_mass = tk.DoubleVar()
BH_Xpos = tk.DoubleVar()
BH_Ypos = tk.DoubleVar()
Photon_num = tk.IntVar()
step_size = tk.DoubleVar()
step_count = tk.IntVar()

# Create Program Title label:
Program_title = tk.Label(mainframe, text="Newtonian Black Hole Simulator", font=("Arial", 24))
Program_title.grid(column=1, row=0, columnspan=4, sticky=(tk.W, tk.E)) # have title span across all columns so it is centered


'''
BLACK HOLE INPUTS
'''

# Create and add the slider input and title for the black hole mass:
tk.Label(mainframe, text="Black hole Mass", font=("Arial", 16)).grid(column=1, row=1, columnspan=4, sticky=(tk.W, tk.E))
BH_mass_entry = tk.Scale(mainframe, variable=BH_mass, from_=0, to=100, tickinterval=10, resolution=0.05, orient=tk.HORIZONTAL)
BH_mass_entry.grid(column=1, row=2, columnspan=4, sticky=(tk.W, tk.E))

# Create and add the inputs and titles for the black hole position:
tk.Label(mainframe, text="Black hole X position", font=("Arial", 12)).grid(column=1, row=3, columnspan=2, sticky=(tk.W, tk.E))
BH_Xpos_entry = tk.Entry(mainframe, textvariable=BH_Xpos)
BH_Xpos_entry.grid(column=1, row=4, columnspan=2, sticky=(tk.W, tk.E))

tk.Label(mainframe, text="Black hole Y position", font=("Arial", 12)).grid(column=3, row=3, columnspan=2, sticky=(tk.W, tk.E))
BH_Ypos_entry = tk.Entry(mainframe, textvariable=BH_Ypos)
BH_Ypos_entry.grid(column=3, row=4, columnspan=2, sticky=(tk.W, tk.E))


'''
RAY INPUTS
'''
tk.Label(mainframe, text="Number of rays", font=("Arial", 16)).grid(column=1, row=6, columnspan=4, sticky=(tk.W, tk.E))
Photon_num_entry = tk.Scale(mainframe, variable=Photon_num, from_=0, to_=500, tickinterval=25, resolution=1, orient=tk.HORIZONTAL)
Photon_num_entry.grid(column=1, row=7, columnspan=4, sticky=(tk.W, tk.E))

'''
STEP INPUTS
'''
tk.Label(mainframe, text="Time step size", font=("Arial", 16)).grid(column=1, row=9, columnspan=4, sticky=(tk.W, tk.E))
step_size_entry = tk.Scale(mainframe, variable=step_size, from_=0.0001, to_=0.05, tickinterval=0.005, resolution=0.0001, orient=tk.HORIZONTAL)
step_size_entry.grid(column=1, row=10, columnspan=4, sticky=(tk.W, tk.E))

tk.Label(mainframe, text="Number of steps", font=("Arial", 16)).grid(column=1, row=11, columnspan=4, sticky=(tk.W, tk.E))
tk.Label(mainframe, text="Set to 0 to calculate number of steps required for 10 seconds of movement", font=("Arial", 12)).grid(column=1, row=12, columnspan=4, sticky=(tk.W, tk.E))
step_count_entry = tk.Scale(mainframe, variable=step_count, from_=0, to_=1_000_000, tickinterval=100_000, resolution=100, orient=tk.HORIZONTAL)
step_count_entry.grid(column=1, row=13, columnspan=4, sticky=(tk.W, tk.E))


'''
SEPERATORS
'''
div_1 = ttk.Separator(mainframe, orient=tk.HORIZONTAL)
div_1.grid(column=1, row=5, columnspan=4, sticky=(tk.W, tk.E))
div_2 = ttk.Separator(mainframe, orient=tk.HORIZONTAL)
div_2.grid(column=1, row=8, columnspan=4, sticky=(tk.W, tk.E))
div_3 = ttk.Separator(mainframe, orient=tk.HORIZONTAL)
div_3.grid(column=1, row=19, columnspan=4, sticky=(tk.W, tk.E))

'''
INFO BUTTON
'''
info_button = tk.Button(mainframe, text="info", font=("Arial", 16), command=LoadInfo)
info_button.grid(column=4, row=0, sticky=tk.E)


tk.Button(mainframe, text="convert to variable", command=Start).grid(column=1, row=20, columnspan=4, sticky=(tk.W, tk.E))

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