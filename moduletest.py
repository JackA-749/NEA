import integrator
import matplotlib.pyplot as plt

# velocity_verlet(vector<double> photon_positions, vector<double> photon_velocities, vector<double> black_hole_position, double minimum_radius, double dt)
black_hole_pos = [5, 5]
schwarzschild_radius = 0.75
dt = 0.001
photon_pos = [0, 0]
photon_vel = [0.5, 2]

x_positions = [photon_pos[0]]
y_positions = [photon_pos[1]]
captured = False
step = 0
while not captured and step < 100000:
    results = integrator.velocity_verlet_dict(photon_pos, photon_vel, black_hole_pos, schwarzschild_radius, dt)
    photon_pos = results["Newcoordinate"]
    photon_vel = results["Newvelocitys"]
    captured = results["captured"]
    x_positions.append(photon_pos[0])
    y_positions.append(photon_pos[1])
    step += 1

    print(f"Step {step}: Photon position: {photon_pos}, Photon velocity: {photon_vel}, Captured: {captured}")

# Plot trajectory
plt.figure(figsize=(8, 8))
plt.plot(x_positions, y_positions, '-o', markersize=3, label='Photon path')
plt.scatter([black_hole_pos[0]], [black_hole_pos[1]], color='red', s=80, label='Black hole')
circle = plt.Circle((black_hole_pos[0], black_hole_pos[1]), schwarzschild_radius, color='red', alpha=0.3)
plt.gca().add_patch(circle)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Photon trajectory near black hole')
plt.axis('equal')
plt.legend()
plt.grid(True)
plt.show()
