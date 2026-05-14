#include <iostream>
#include <cmath>
#include <vector>
using namespace std;

// Global variables / physical constants
int G = 1;
int M = 10;

// Create a structure to store the results of a step in the simulation
struct stepresult {
    bool captured;

    vector<double> Newcoordinate;
    vector<double> Newvelocitys;
};

// declare the names of functions within the file
vector<double> gravity_accel(vector<double> photon_positions, vector<double> black_hole_position);
stepresult velocity_verlet(vector<double> photon_positions, vector<double> photon_velocities, vector<double> black_hole_position, double minimum_radius, double dt);
vector<double> get_dist (vector<double> photon_positions, vector<double> black_hole_position);

// main loop
int main() {
    return 0;
}

// define the behaviours of functions in the file

vector<double> get_dist (vector<double> photon_positions, vector<double> black_hole_position) {
        // get distances from black hole in each direction
        double x_dist = photon_positions[0] - black_hole_position[0];
        double y_dist = photon_positions[1] - black_hole_position[1];
        
        // find the distance between the photon and black hole using pythagoras
        double distance = sqrt((x_dist * x_dist) + (y_dist * y_dist));

        return vector<double> {x_dist, y_dist, distance};
}

vector<double> gravity_accel(vector<double> photon_positions, vector<double> black_hole_position) {
    /* calculate the Acceleration of a light ray across towards the black hole */

    vector<double> distances = get_dist(photon_positions, black_hole_position);
    double x_dist = distances[0];
    double y_dist = distances[1];
    double total_distance = distances[2];

    // find the unit vector of the acceleration, so that the acceleration can be split into its components
    double factor = (G*M) / (total_distance * total_distance * total_distance);

    //break the acceleration into its horizontal and vertical components
    double x_accel = factor * x_dist;
    double y_accel = factor * y_dist;

    vector<double> accelerations = {x_accel, y_accel};
    return accelerations;

}

stepresult velocity_verlet(vector<double> photon_positions, vector<double> photon_velocities, vector<double> black_hole_position, double minimum_radius, double dt) {

    // Create the result structure to store required values
    stepresult verlet_results;

    // get the distance from the black hole 
    vector<double> distances = get_dist(photon_positions, black_hole_position);
    double total_distance = distances[2];

    /*
    use the distance from the black hole to check if the photon is within the minimum / schwarzschild radius
    */
    if (total_distance < minimum_radius) {
        verlet_results.captured = true;
    } 
    else {
        verlet_results.captured = false;
    };

    /*
    Perform the velocity verlet steps
    */

    // get acceleration for this step
    vector<double> accelerations = gravity_accel(photon_positions, black_hole_position); // {x_accel, y_accel}

    // calculate new coordinates
    double new_x_position = photon_positions[0] + photon_velocities[0] * dt + 0.5 * accelerations[0] * (dt * dt);
    double new_y_position = photon_positions[1] + photon_velocities[1] * dt + 0.5 * accelerations[1] * (dt * dt);

    // calculate acceleration at new position
    vector<double> new_accelerations = gravity_accel(vector<double> {new_x_position, new_y_position}, black_hole_position); // {x_accel, y_accel}

    // calculate new velocities
    double new_x_velocity = photon_velocities[0] + 0.5 * (accelerations[0] + new_accelerations[0]) * dt;
    double new_y_velocity = photon_velocities[1] + 0.5 * (accelerations[1] + new_accelerations[1]) * dt;

    // add results to verlet_results structure to be returned
    verlet_results.Newcoordinate[0] = new_x_position;
    verlet_results.Newcoordinate[1] = new_y_position;
    verlet_results.Newvelocitys[0] = new_x_velocity;
    verlet_results.Newvelocitys[1] = new_y_velocity;

    return verlet_results;
}