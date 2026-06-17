import integrator
import numpy as np

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
        self.next_pos = integrator.elocity_verlet(before_step, [self.x_vel, self.y_vel], black_hole_position, time_step, BH_Mass)
        self.last_pos = before_step
        positions = [self.last_pos, self.next_pos]

class circular_queue(): # circular queue structure to handle order of photon updates
    def __init__(self, size):
        self._array = np.empty(shape=size, dtype=object)
        self._front_pointer = 0
        self._rear_pointer = size-1
        self._max_length = size
    
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
        if len(self._array) == 0:
            print("Queue is already empty, exiting function")
            exit()
        x = self._array[self._front_pointer]
        self._front_pointer += 1
        if self._front_pointer+1 == self._max_length:
            self._front_pointer = 0
        return x
    
    def add_new_item_to_list(self, item):
        #check if the queue is full
        if self._rear_pointer+1 == self._max_length:
            print("Queue is already full, exiting function")
            exit()
        self._rear_pointer += 1
        self._array[self._rear_pointer] = item


    def check_last_item(self):
        print(self._rear_pointer)
        print(self._max_length)
        return self._array[self._rear_pointer]

    def show_queue(self):
        return self._array


def run_simulation(BlackHoleMass, BlackHoleX, BlackHoleY, photon_number, dt, num_steps):
    #set required variable for integrator to globals
    global black_hole_position
    black_hole_position = [BlackHoleX, BlackHoleY]
    global BH_Mass
    BH_mass = BlackHoleMass
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
        photons.append(Photon([0.0, y_vals[i].item()], [0.0,0.0])) # add all photons to the the list with correct coordinates

    #Add all photons to the queue
    queue.add_photons_to_queue(photons)

    simulation_complete = False
    steps_taken = 0 # keep track of the number of steps aken so the simulation can end
    #loop until the simulation is complete
    while not simulation_complete:
        last_positions = [] # create an empty list to store the past positions of photons for this loop so they can be passed into the plot update
        new_positions = [] # create an empty list to store the new positions of photons for this loop so they can be passed into the plot update
        #iterate through the entire queue of photons once to get new values for the plot
        for j in range(0, (PHOTON_NUM-1)):
            current_photon = queue.get_first_item()
            last_positions.append(current_photon.next_pos)
            '''current_photon = integrator.velocity_verlet(current_photon)
            new_positions.append(current_photon.next_pos)
            update_plot(last_positions, new_positions)'''
        steps_taken += 1
        print(steps_taken)
        if steps_taken == num_steps:
            simulation_complete = True

    print(last_positions)


def update_plot(last_positions, new_positions):
    print("plot update ran")