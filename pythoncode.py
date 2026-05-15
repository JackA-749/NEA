import matplotlib as plt
import numpy as np
import math
import integrator


''' Initialise all the parameters '''

# scale factor and gravitational constant G
global Scale_factor
Scale_factor = 1.25760695 * (10 ** 10)

global G
G = 6.67430 * (10 ** -11) * (Scale_factor ** 3)  # Gravitational constant

global c
c = 299792458 * Scale_factor  # Speed of light in m/s

# screen size
WIDTH, HEIGHT = 800, 800


''' SETUP CLASSES '''
class Photon():
    def __init__(self, position, velocity, acceleration, colour, captured=False):
        self.position = position # {x, y}
        self.velocity = velocity # {vx, vy}
        self.acceleration = acceleration # {ax, ay}
        self.colour = colour # {r, g, b}
        self.captured = captured # Boolean indicating if the photon is captured

    def check_captured(self, black_hole):
        # Check if the photon is within the schwarzschild radius of the black hole
        pass

    def adjust_colour(self):
        # Adjust the colour of the photon based on its velocity and position
        pass


class BlackHole():
    def __init__(self, position, mass):
        self.position = position
        self.mass = mass
        self.schwarzschild_radius = 2 * G * self.mass / (c ** 2)


class simulation_screen():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.photons = [] #list to store all the photons shown in the simulation
        self.black_holes = [] #list to store all the black holes shown in the simulation


''' FUNCTIONS '''
#main loop for all object handling
def main():
    print("Main loop run")


if __name__ == "__main__":
    main()
