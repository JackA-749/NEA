import tkinter as tk
from tkinter import ttk
from math import floor
import Simulation
import traceback

def Start(*args):
    try:
        BlackHoleMass = BH_mass.get()
        BlackHoleX = BH_Xpos.get()
        BlackHoleY = BH_Ypos.get()
        photon_number = Photon_num.get()
        dt = step_size.get()
        num_steps = step_count.get()
        if num_steps == 0:
            num_steps = floor(10/dt)
        global photon_states
        photon_states = Simulation.run_simulation(BlackHoleMass, BlackHoleX, BlackHoleY, photon_number, dt, num_steps) #[Captive, (active / escaped)]
        global param_dict
        param_dict = {
            "Black hole mass": BlackHoleMass,
            "Black hole X": BlackHoleX,
            "Black hole Y": BlackHoleY,
            "Photon Number": photon_number,
            "Step size": dt,
            "Step count": num_steps
        }
        Show_end_screen()
    except Exception as e:
        print(f"Error occurred: {e}")
        traceback.print_exc()

def Export_results():
    import json
    from tkinter import filedialog, messagebox
    results = {
        "Captured": photon_states[0],
        "Escaped": photon_states[1],
        "Parameters": param_dict
    }

    result_json = json.dumps(results)

    # Open a window for user to select download location
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        title="Choose where to save your file"
    )

    if file_path: # if the user selected a location
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(result_json) # write the json object to the file

            messagebox.showinfo("Success", f"File saved successfully to:\n{file_path}") #display a message to show it worked

        except Exception as e:
            messagebox.showinfo(f"Error could not save file: {e}")

def Show_end_screen():
    # set up window to hold all elements on results screen at the end of the simulation
    End_window = tk.Toplevel(master=root)
    End_window.title("Results")
    End_window.geometry("720x810")

    # Create a frame to attatch all elements to
    Endframe = ttk.Frame(End_window, padding=(3, 3, 12, 12))
    Endframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

    # Page title
    End_title = tk.Label(Endframe, text="Simulation results", font=("Arial", 24))
    End_title.grid(column=0, row=0, columnspan=4, sticky=(tk.N, tk.W, tk.E, tk.S))

    # Section titles
    Escaped_title = tk.Label(Endframe, text="Escaped photons:", font=("Arial", 18))
    Escaped_title.grid(column=0, row=1)

    Captured_title = tk.Label(Endframe, text="Captured photons:", font=("Arial", 18))
    Captured_title.grid(column=1, row=1)
    
    # Section subtitles
    Escaped_subtitle = tk.Label(Endframe, text="Some active photons will be counted as escaped if simulation was ended early", font=("Arial", 10))
    Escaped_subtitle.grid(column=0, row=2, sticky=(tk.W, tk.E))

    # Info labels
    Escaped_count_label = tk.Label(Endframe, text=(f'{photon_states[1]}'), font=("Arial", 24))
    Escaped_count_label.grid(column=0, row=3, sticky=(tk.W, tk.E))

    Captured_count_label = tk.Label(Endframe, text=(f'{photon_states[0]}'), font=("Arial", 24))
    Captured_count_label.grid(column=1, row=3, sticky=(tk.W, tk.E))

    # Export button
    Export_button = tk.Button(Endframe, text="Export results", command=Export_results).grid(column=0, row=20, columnspan=2, sticky=(tk.W, tk.E))



    # Give each column in the mainframe a weight so columnspan centering works
    Endframe.columnconfigure(1, weight=1)
    Endframe.columnconfigure(2, weight=1)
    Endframe.columnconfigure(3, weight=1)
    Endframe.columnconfigure(4, weight=1)


    

def LoadInfo(*args):
    # When the User clicks the information button, this function will open a new window with the information about the program and how to use it.
    Info_window = tk.Toplevel(master=root)
    Info_window.title("Information")
    Info_window.geometry("720x810")

    # Create a frame to attatch all elements to
    InfoFrame = ttk.Frame(Info_window, padding=(3, 3, 12, 12))
    InfoFrame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

    # Page title
    info_title = tk.Label(InfoFrame, text="Parameter Information", font=("Arial", 24))
    info_title.grid(column=1, row=0, columnspan=2, sticky=(tk.W, tk.E)) # span the title across all columns so it is centered

    # Parameter Titles:
    mass_title = tk.Label(InfoFrame, text="Black hole mass: ", font=("Arial", 18))
    mass_title.grid(column=0, row=1)

    # Parameter descriptions:
    mass_description = tk.Label(InfoFrame, text="The mass of the black hole determines the the magnitude of acceleration that nearby objects will experience and increases the size of the Schwarzschild radius")
    mass_description.bind('<configure>', lambda e: mass_description.config(wraplength=mass_description.winfo_width()))
    mass_description.grid(column=1, row=1)


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

#give each variable a default value to eliminate empty field errors:
BH_mass = tk.DoubleVar(value=10.0)
BH_Xpos = tk.DoubleVar(value=0.0)
BH_Ypos = tk.DoubleVar(value=0.0)
Photon_num = tk.IntVar(value=100)
step_size = tk.DoubleVar(value=0.01)
step_count = tk.IntVar(value=0)

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
Photon_num_entry = tk.Scale(mainframe, variable=Photon_num, from_=1, to_=500, tickinterval=25, resolution=1, orient=tk.HORIZONTAL)
Photon_num_entry.grid(column=1, row=7, columnspan=4, sticky=(tk.W, tk.E))

'''
STEP INPUTS
'''
tk.Label(mainframe, text="Time step size", font=("Arial", 16)).grid(column=1, row=9, columnspan=4, sticky=(tk.W, tk.E))
step_size_entry = tk.Scale(mainframe, variable=step_size, from_=0.0001, to_=0.05, tickinterval=0.005, resolution=0.0001, orient=tk.HORIZONTAL)
step_size_entry.grid(column=1, row=10, columnspan=4, sticky=(tk.W, tk.E))

tk.Label(mainframe, text="Number of steps", font=("Arial", 16)).grid(column=1, row=11, columnspan=4, sticky=(tk.W, tk.E))
tk.Label(mainframe, text="Set to 0 to calculate number of steps required for 10 seconds of movement", font=("Arial", 12)).grid(column=1, row=12, columnspan=4, sticky=(tk.W, tk.E))
step_count_entry = tk.Scale(mainframe, variable=step_count, from_=0, to_=100_000, tickinterval=10_000, resolution=100, orient=tk.HORIZONTAL)
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


tk.Button(mainframe, text="Run Simulation", command=Start).grid(column=1, row=20, columnspan=4, sticky=(tk.W, tk.E))

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