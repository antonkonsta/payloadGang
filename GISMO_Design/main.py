''' NOTEd
'''

from func_def import simulate_smd, simulate_descent
import ODEs as m 
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

# Descent settings
deployment_height_ft = 450 # Feet
initial_deployment_velocity_fts = 13 # Feet/s
mass_payload_lb = 10 # Pounds

# Nosecone info
drag_coefficient = 0.3

# Spring Mass Damper settings
mass_capsule_lb = 0.5 # lbs
initial_displacement_in = 0 # inches
impact_velocity = 6 # remove this later


# Simulation Settings
max_displacement_in = 8 # inches
simulation_duration = 3# Seconds
data_points = 1000 # Number of data points to be taken

# Miscellaneous Constants
g = 9.81 # Gravity
rho = 1.225 # Air density in kg/m^3

# Convert to SI units
deployment_height_m = deployment_height_ft * 0.3048
initial_deployment_velocity_ms = initial_deployment_velocity_fts* 0.3048
mass_payload_kg = mass_payload_lb * 0.45359237
mass_capsule_kg = mass_capsule_lb * 0.45359237
initial_displacement_m = initial_displacement_in * 0.0254
max_displacement_m = max_displacement_in * 0.0254

# Array of time points for simulations
t = np.linspace(0, simulation_duration, data_points)

displacement, velocity, acceleration = simulate_smd(initial_displacement_m, initial_deployment_velocity_ms, mass_capsule_kg, 5, 50, t)

# Convert units back to imperial
displacement_result = displacement  * 39.3701 
velocity_result = velocity * 3.28084
G_Force_result = acceleration * 0.101972

# Plot displacement vs. time
plt.figure(figsize=(10, 8))
plt.subplot(2, 2, 1)
plt.plot(t, displacement_result)
plt.xlabel('Time (s)')
plt.ylabel('Displacement (in)')
plt.title('Displacement vs. Time')

# Plot acceleration vs. time
plt.subplot(2, 2, 3)
plt.plot(t, G_Force_result)
plt.xlabel('Time (s)')
plt.ylabel('G Force')
plt.title('G Force vs. Time')


plt.tight_layout()  # This will ensure the plots are not overlapping
plt.show()
