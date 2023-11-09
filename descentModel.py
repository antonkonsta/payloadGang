import numpy as np
import matplotlib.pyplot as plt

# Set up your variables here
mass_kg = 2.5  # Mass in kilograms
diameter_m = 0.127  # Diameter in meters
height_m = 130  # Initial height in meters
dt = 0.001  # Time step in seconds
initial_velocity_m_per_s = 3.9624  # Initial velocity in m/s
F_thrust = 10  # Thrust force in Newtons

# Constants
g = 9.81  # Acceleration due to gravity in m/s^2
rho = 1.225  # Air density in kg/m^3
A = np.pi * (diameter_m / 2)**2  # Cross-sectional area in m^2
drag_coefficient = 0.47  # Drag coefficient for a sphere

# Lists to store height and velocity values
heights = []
velocities = []

# Initialize velocity and position
velocity = initial_velocity_m_per_s
position = height_m

# Simulation loop
while position > 0:
    # Force calculations
    F_gravity = mass_kg * g
    F_drag = 0.5 * drag_coefficient * rho * A * velocity**2
    
    # If thrust is active, subtract it from the net force
    net_force = F_gravity - F_drag - F_thrust

    # Acceleration (net force divided by mass)
    acceleration = net_force / mass_kg

    # Update velocity and position
    velocity += acceleration * dt
    position -= velocity * dt

    # Store the current height and velocity
    heights.append(position)
    velocities.append(velocity)

# Plot
plt.figure(figsize=(10, 5))

# Plot velocity vs height
plt.plot(velocities, heights)
plt.xlabel('Velocity (m/s)')
plt.ylabel('Height (m)')
plt.title('Velocity vs. Height During Descent')
plt.gca().invert_yaxis()  # Invert y-axis to show descent from initial height to ground
plt.grid(True)
plt.show()
