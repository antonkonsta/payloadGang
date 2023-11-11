import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

rho = 1.225  # Air density at sea level in kg/m^3
mass = 2.0   # Mass of the object in kg
area = 0.05  # Cross-sectional area in m^2
drag_coefficient = 0.3
g = 9.8
# Modified function to compute the derivatives of both velocity and position
def model_with_position(y, t, rho, mass, drag_coefficient, area):
    v, h = y  # Unpack the current values of velocity and height
    # Drag force: Fd = 1/2 * rho * v^2 * Cd * A
    drag_force = 0.5 * rho * abs(v) * v * drag_coefficient * area  # Abs(v) ensures correct direction of drag
    # Net force
    net_force = mass * g - drag_force
    # Acceleration
    dvdt = net_force / mass
    # Derivative of height is the velocity
    dhdt = -v  # Negative because as the object falls, height decreases
    return [dvdt, dhdt]

# Initial conditions: initial velocity and initial height
initial_height = 100.0  # Initial height in meters

# Initial state vector [velocity, height]
initial_state = [4, 100]

time = np.linspace(0, 10, 1000)

# Solving the system of differential equations
solution = odeint(model_with_position, initial_state, time, args=(rho, mass, drag_coefficient, area))

# Extracting velocity and height from the solution
velocity_with_height = solution[:, 0]
height_with_time = solution[:, 1]

# Plotting the results
plt.figure(figsize=(12, 6))

# Velocity plot
plt.subplot(1, 2, 1)
plt.plot(time, velocity_with_height)
plt.xlabel('Time (seconds)')
plt.ylabel('Velocity (m/s)')
plt.title('Velocity over Time')
plt.grid(True)

# Height plot
plt.subplot(1, 2, 2)
plt.plot(time, height_with_time)
plt.xlabel('Time (seconds)')
plt.ylabel('Height (meters)')
plt.title('Height over Time')
plt.grid(True)

plt.tight_layout()
plt.show()
