from tkinter import *
from tkinter import ttk

def Start(*args):
    BlackHoleMass = BH_mass.get()
    print(BlackHoleMass)

root = Tk()
root.title("Black Hole Sim")

mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

BH_mass = StringVar()
BH_mass = ttk.Entry(mainframe, width=7, textvariable=BH_mass)
BH_mass.grid(column=2, row=1, sticky=(W, E))

meters = StringVar()
ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))

ttk.Button(mainframe, text="convert to variable", command=Start).grid(column=3, row=3, sticky=W)

ttk.Label(mainframe, text="Black hole Mass").grid(column=3, row=1, sticky=W)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(2, weight=1)
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

BH_mass.focus()
root.bind("<Return>", Start)

root.mainloop()