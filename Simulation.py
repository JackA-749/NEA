import integrator
import numpy as np
import matplotlib.pyplot as plt

# Create a photon class to handle all information
class Photon:
    def __init__(self, position, velocities):
        self.last_pos = []
        self.x_vel = velocities[0]
        self.y_vel = velocities[1]
        self.iscaptured = False # all photons start off as not captured
        self.next_pos = position #[x,y]

    def step_forward(self):
        before_step = self.next_pos

        result = integrator.velocity_verlet(before_step, [self.x_vel, self.y_vel], black_hole_position, time_step, BH_Mass)

        self.next_pos = result.Newcoordinate
        self.iscaptured = result.captured

        self.x_vel = result.Newvelocitys[0]
        self.y_vel = result.Newvelocitys[1]

        self.last_pos = before_step
        positions = [self.last_pos, self.next_pos]

        return positions

class circular_queue(): # circular queue structure to handle order of photon updates
    def __init__(self, size):
        self._array = np.empty(shape=size, dtype=object)
        self._front_pointer = 0
        self._rear_pointer = size-1
        self._max_length = size
        self.current_size = size
    
    def add_photons_to_queue(self, photons):
        #add all photons passed in
        count = 0
        for photon in photons:
            self._array[count] = photon
            count += 1
        #move rear pointer down until it is on a space with an object
        valid = False
        while not valid:
            if self._array[self._rear_pointer] == None: #if the space at rear pointer is empty
                self._rear_pointer -= 1
            else:
                valid = True
    
    def get_first_item(self):
        #check queue is not already empty
        if self.current_size == 0:
            print("Queue is already empty, exiting function")
            exit()
        x = self._array[self._front_pointer] # get the item at the front of the queue
        self._array[self._front_pointer] = None #remove the item from the queue
        self.current_size -= 1
        self._front_pointer = (self._front_pointer + 1) % self._max_length #move the front pointer to the next item in the queue and loop back to beginning if it is at the end of the queue
        return x
    
    def add_new_item_to_list(self, item):
        #check if the queue is full
        if self.current_size >= self._max_length:
            print("Queue is already full, exiting function")
            exit()
        self._rear_pointer = (self._rear_pointer + 1) % self._max_length #move the rear pointer to the next item in the queue and loop back to beginning if it is at the end of the queue
        self._array[self._rear_pointer] = item
        self.current_size += 1


    def check_last_item(self):
        print(self._rear_pointer)
        print(self._max_length)
        return self._array[self._rear_pointer]

    def show_queue(self):
        return self._array
    
class Plot:
    def __init__(self):
        fig, self.plot = plt.subplots()
        self.plot.set_xlabel("X position")
        self.plot.set_ylabel("Y position")
        self.plot.set_title("Black hole simulation")

        # Set plot bounds
        self.plot.set_xlim(-15, 15)
        self.plot.set_ylim(-5, 15)

        #set schwarzschild radius
        Schwarzschild = 2 * BH_Mass

        # Draw the black hole on the plot
        self.black_hole = plt.Circle((black_hole_position[0], black_hole_position[1]), (0.3*Schwarzschild), color="Black", fill=True)
        self.plot.add_patch(self.black_hole)

        # Draw the schwarzschild radius
        self.radius = plt.Circle((black_hole_position[0], black_hole_position[1]), Schwarzschild, color="red", fill=False)
        self.plot.add_patch(self.radius)

        # Create an empty scatter plot for the photons
        self.scatter_plot = self.plot.scatter([], [], color="blue", s=15, label="photons")

        self.plot.set_aspect('equal')
        plt.legend()

    def Update(self, last_positions, new_positions):
        if new_positions:
            #add new photon positions to plot
            self.scatter_plot.set_offsets(new_positions)

        # redraw the new, updated plot
        plt.draw()
        plt.pause(0.001) # add a short delay to let GUI update 


def run_simulation(BlackHoleMass, BlackHoleX, BlackHoleY, photon_number, dt, num_steps):
    #set required variable for integrator to globals
    global black_hole_position
    black_hole_position = [BlackHoleX, BlackHoleY]
    global BH_Mass
    BH_Mass = BlackHoleMass
    global time_step
    time_step = dt
    global PHOTON_NUM
    PHOTON_NUM = photon_number

    #Create the queue
    queue = circular_queue(PHOTON_NUM)

    #create a list of evenly spaced photons
    photons = [] # empty list to store photons
    y_vals = np.linspace(0, 10, PHOTON_NUM) # creates a list of evenly spaced y-values for photons along the length of the y axis

    for i in range(0, PHOTON_NUM):
        photons.append(Photon([-10.0, y_vals[i].item()], [1.0,0.0])) # add all photons to the the list with correct coordinates

    #Add all photons to the queue
    queue.add_photons_to_queue(photons)

    #Create the plot to show photon paths
    plot = Plot()

    plt.ion() # Enable interactive mode so the plot updates instantly each time a change is made

    simulation_complete = False
    steps_taken = 0 # keep track of the number of steps aken so the simulation can end
    #loop until the simulation is complete

    while not simulation_complete:

        last_positions = [] # create an empty list to store the past positions of photons for this loop so they can be passed into the plot update
        new_positions = [] # create an empty list to store the new positions of photons for this loop so they can be passed into the plot update

        #iterate through the entire queue of photons once to get new values for the plot
        for j in range(0, (PHOTON_NUM)):
            current_photon = queue.get_first_item()

            if not current_photon.iscaptured:
                positions = current_photon.step_forward() # get the new positions of the photon
                last_positions.append(positions[0]) # add the last position of the photon to the list of last positions
                new_positions.append(positions[1]) # add the new position of the photon to the list of new positions
            else:
                new_positions.append(current_photon.next_pos)

            # Add the photon back into the queue
            queue.add_new_item_to_list(current_photon)
        
        plot.Update(last_positions, new_positions)
        steps_taken += 1
        if steps_taken >= num_steps:
            simulation_complete = True
            print("simulation ran successfully")

plt.ioff()
plt.show()