#include <iostream>
#include <sstream>
#include <cmath>
#include <vector>

// Adding pybind
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
namespace py = pybind11;
using namespace pybind11::literals;

using namespace std;

// Global variables / physical constants
int G = 5.27191743 * pow(10, -21);
int C = 299792458

// Artificial decay factor to make the photon spiral inward over time.
// This is a simulation aid; without energy loss, a Newtonian orbit can remain stable.
const double ORBITAL_DECAY = 0.9999;


// Create a structure to store the results of a step in the simulation
struct stepresult {
    bool captured;

    vector<double> Newcoordinate;
    vector<double> Newvelocitys;
};

// declare the names of functions within the file
vector<double> gravity_accel(vector<double> photon_positions, vector<double> black_hole_position, int BH_Mass);
stepresult velocity_verlet(vector<double> photon_positions, vector<double> photon_velocities, vector<double> black_hole_position, double minimum_radius, double dt, int BH_Mass);
vector<double> get_dist (vector<double> photon_positions, vector<double> black_hole_position);

// main loop
int main() {
    return 0;
}

// define the behaviours of functions in the file

vector<double> get_dist (vector<double> photon_positions, vector<double> black_hole_position) {
        // get distances from black hole in each direction
        double x_dist = black_hole_position[0] - photon_positions[0];
        double y_dist = black_hole_position[1] - photon_positions[1];
        
        // find the distance between the photon and black hole using pythagoras
        double distance = sqrt((x_dist * x_dist) + (y_dist * y_dist));

        return vector<double> {x_dist, y_dist, distance};
}

vector<double> gravity_accel(vector<double> photon_positions, vector<double> black_hole_position, int BH_Mass) {
    /* calculate the Acceleration of a light ray across towards the black hole */

    vector<double> distances = get_dist(photon_positions, black_hole_position);
    double x_dist = distances[0];
    double y_dist = distances[1];
    double total_distance = distances[2];

    // find the unit vector of the acceleration, so that the acceleration can be split into its components
    double factor = (G*BH_Mass) / (total_distance * total_distance * total_distance);

    //break the acceleration into its horizontal and vertical components
    double x_accel = factor * x_dist;
    double y_accel = factor * y_dist;

    vector<double> accelerations = {x_accel, y_accel};
    return accelerations;

}

stepresult velocity_verlet(vector<double> photon_positions, vector<double> photon_velocities, vector<double> black_hole_position, double minimum_radius, double dt, int BH_Mass) {

    // Create the result structure to store required values
    stepresult verlet_results;
    verlet_results.Newcoordinate.resize(2);
    verlet_results.Newvelocitys.resize(2);

    // Calculate Schwarzschild radius
    double minimum_radius = (2*G*BH_Mass) / C*C

    // get the distance from the black hole 
    vector<double> distances = get_dist(photon_positions, black_hole_position); // {x_dist, y_dist, distance}
    double total_distance = distances[2];

    if (total_distance <= minimum_radius || total_distance <= 1e-12) {
        verlet_results.captured = true;
        verlet_results.Newcoordinate[0] = photon_positions[0];
        verlet_results.Newcoordinate[1] = photon_positions[1];
        verlet_results.Newvelocitys[0] = photon_velocities[0];
        verlet_results.Newvelocitys[1] = photon_velocities[1];
        return verlet_results;
    }

    verlet_results.captured = false;

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

    // Apply a small decay to the velocity so the orbit can spiral inward.
    // This is an artificial effect to model capture rather than a true photon geodesic.
    new_x_velocity *= ORBITAL_DECAY;
    new_y_velocity *= ORBITAL_DECAY;

    // detect capture after the step if the photon moved inside the radius
    vector<double> new_distances = get_dist(vector<double>{new_x_position, new_y_position}, black_hole_position);
    if (new_distances[2] <= minimum_radius) {
        verlet_results.captured = true;
    }

    // add results to verlet_results structure to be returned
    verlet_results.Newcoordinate[0] = new_x_position;
    verlet_results.Newcoordinate[1] = new_y_position;
    verlet_results.Newvelocitys[0] = new_x_velocity;
    verlet_results.Newvelocitys[1] = new_y_velocity;

    return verlet_results;
}

// setting up the pybindmodule to expose the C++ to python
PYBIND11_MODULE(integrator, m) {
    m.doc() = "Module containing distance and gravity calculators as well as numerical integrator functions and custom classes to ensure compatability"; // Module docstring

    // Expose the integrator function to python:
    m.def("velocity_verlet", &velocity_verlet, "Velocity verlet numerical integrator for photons", py::arg("photon_positions"), py::arg("photon_velocities"), py::arg("black_hole_position"), py::arg("minimum_radius"), py::arg("dt"));

    // Expose the stepresult class so that it can be passed between and interpretted by both languages
    py::class_<stepresult>(m, "stepresult")
        .def_readwrite("captured", &stepresult::captured)
        .def_readwrite("Newcoordinate", &stepresult::Newcoordinate)
        .def_readwrite("Newvelocitys", &stepresult::Newvelocitys)
        .def("__repr__", [](const stepresult &s) {
            std::ostringstream oss;
            oss << "stepresult(captured=" << std::boolalpha << s.captured
                << ", Newcoordinate=[" << s.Newcoordinate[0] << ", " << s.Newcoordinate[1] << "]"
                << ", Newvelocitys=[" << s.Newvelocitys[0] << ", " << s.Newvelocitys[1] << "])";
            return oss.str();
        });

    m.def("velocity_verlet_dict",
          [](const std::vector<double> &photon_positions,
             const std::vector<double> &photon_velocities,
             const std::vector<double> &black_hole_position,
             double minimum_radius,
             double dt) {
              stepresult res = velocity_verlet(photon_positions, photon_velocities, black_hole_position, minimum_radius, dt);
              return py::dict("captured"_a = res.captured,
                              "Newcoordinate"_a = res.Newcoordinate,
                              "Newvelocitys"_a = res.Newvelocitys);
          },
          "Velocity verlet numerical integrator returning a dict",
          py::arg("photon_positions"), py::arg("photon_velocities"),
          py::arg("black_hole_position"), py::arg("minimum_radius"),
          py::arg("dt"));
}