import integrator
import numpy as np
import matplotlib.pyplot as plt

# Create a photon class to handle all information
class Photon:
    def __init__(self, position, velocities):
        self.x_history = [position[0]]
        self.y_history = [position[1]]
        self.x_vel = velocities[0]
        self.y_vel = velocities[1]
        self.iscaptured = False # all photons start off as not captured
        self.next_pos = position #[x,y]

        self.step_counter = 0 # count to track the number of steps for sampling

    def step_forward(self):
        if not self.iscaptured:
            before_step = self.next_pos

            result = integrator.velocity_verlet(
                before_step, [self.x_vel, self.y_vel], black_hole_position, time_step, BH_Mass
                )

            self.next_pos = result.Newcoordinate
            self.iscaptured = result.captured

            self.x_vel = result.Newvelocitys[0]
            self.y_vel = result.Newvelocitys[1]

            self.last_pos = before_step

            self.step_counter += 1
            # only record position to history every 25 steps to improve memory efficiency
            if self.step_counter % 25 == 0 or self.iscaptured:
                self.x_history.append(self.next_pos[0])
                self.y_history.append(self.next_pos[1])

class circular_queue(): # circular queue structure to handle order of photon updates
    def __init__(self, size):
        self._array = np.empty(shape=size, dtype=object)
        self._front_pointer = 0
        self._rear_pointer = size-1
        self._max_length = size
        self.current_size = 0
    
    def add_photons_to_queue(self, photons):
        #add all photons passed in
        for photon in photons:
            self._array[self.current_size] = photon
            self.current_size += 1
            if self.current_size > self._max_length:
                raise IndexError("Queue is already full, cannot enqueue another item.")
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
            raise IndexError("Queue is already empty, cannot dequeue item.")
        x = self._array[self._front_pointer] # get the item at the front of the queue
        self._array[self._front_pointer] = None #remove the item from the queue
        self.current_size -= 1
        self._front_pointer = (self._front_pointer + 1) % self._max_length #move the front pointer to the next item in the queue and loop back to beginning if it is at the end of the queue
        return x
    
    def add_new_item_to_list(self, item):
        #check if the queue is full
        if self.current_size >= self._max_length:
            raise IndexError("Queue is already full, cannot enqueue another item.")
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

        # Set plot bounds based on black hole mass
        self.plot.set_xlim(-(8*BH_Mass), (8*BH_Mass))
        self.plot.set_ylim(-(8*BH_Mass), (8*BH_Mass))

        #set schwarzschild radius
        Schwarzschild = 2 * BH_Mass

        # Draw the black hole on the plot
        self.black_hole = plt.Circle((black_hole_position[0], black_hole_position[1]), (0.3*Schwarzschild), color="Black", fill=True)
        self.plot.add_patch(self.black_hole)

        # Draw the schwarzschild radius
        self.radius = plt.Circle((black_hole_position[0], black_hole_position[1]), Schwarzschild, color="red", fill=False)
        self.plot.add_patch(self.radius)

        # Create a line per photon to handle trajerctories
        self.lines = []
        for x in range(PHOTON_NUM):
            line, = self.plot.plot([], [], color='blue', alpha=0.6, linewidth=1.2)
            self.lines.append(line)

        self.plot.set_aspect('equal')

    def update_photon_lines(self, index, photon_x_history, photon_y_history):
        self.lines[index].set_data(photon_x_history, photon_y_history) #update the coordinates of the line

    def refresh_plot(self):
        # redraw the new, updated plot
        plt.draw()
        plt.pause(0.001) # add a short delay to let GUI update 


def run_simulation(BlackHoleMass, BlackHoleX, BlackHoleY, photon_number, dt, num_steps):
    #set required variable for integrator to globals
    global black_hole_position, BH_Mass, time_step, PHOTON_NUM
    black_hole_position = [BlackHoleX, BlackHoleY]
    BH_Mass = BlackHoleMass
    time_step = dt
    PHOTON_NUM = photon_number

    #Create the queue
    queue = circular_queue(PHOTON_NUM)

    # lists to track photon states
    captured_photons = []

    #create a list of evenly spaced photons
    photons = [] # empty list to store photons
    y_vals = np.linspace(-(8*BH_Mass), (8*BH_Mass), PHOTON_NUM) # creates a list of evenly spaced y-values for photons along the length of the y axis

    for i in range(0, PHOTON_NUM):
        photons.append(Photon([-(8*BH_Mass), y_vals[i].item()], [1.0,0.0])) # add all photons to the the list with correct coordinates

    #Add all photons to the queue
    queue.add_photons_to_queue(photons)

    #Create the plot to show photon paths
    plot = Plot()

    plt.ion() # Enable interactive mode so the plot updates instantly each time a change is made

    simulation_complete = False
    steps_taken = 0 # keep track of the number of steps aken so the simulation can end
    #loop until the simulation is complete

    while not simulation_complete:

        #iterate through the entire queue of photons once to get new values for the plot
        for j in range(PHOTON_NUM):
            current_photon = queue.get_first_item()

            if not current_photon.iscaptured:
                current_photon.step_forward() # update the photon positions

            else:
                captured_photons.append(current_photon)

            plot.update_photon_lines(j, current_photon.x_history, current_photon.y_history)
        
            # Add the photon back into the queue
            queue.add_new_item_to_list(current_photon)


        if steps_taken % 5 == 0: #update plot every 5 steps
            plot.refresh_plot() # refresh the plot once all line segments are drawn
        steps_taken += 1
        if steps_taken >= num_steps:
            simulation_complete = True
            print("simulation ran successfully")
            active_photons = PHOTON_NUM - len(captured_photons)
            return [len(captured_photons), active_photons]
            

        print(f'steps_taken: {steps_taken}!')

plt.ioff()
plt.show()