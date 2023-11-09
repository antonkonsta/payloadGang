import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Differential equations for the spring-mass-damper system
def system_derivatives(y, t, m, c, k):
    x, v = y
    dxdt = v
    dvdt = (-c * v - k * x) / m + g  # adding gravity
    return [dxdt, dvdt]

# Known parameters
g = 9.81  # gravitational acceleration (m/s^2)
m = float(input("Enter the mass of the system (kg): "))
impact_velocity = float(input("Enter the velocity at impact (m/s): "))
max_allowable_accel = float(input("Enter the maximum allowable acceleration (m/s^2): "))

# Time array for simulation
t = np.linspace(0, 10, 1000)  # Adjust as necessary
# Initial conditions: [initial displacement, initial velocity]
initial_conditions = [0, impact_velocity]

# Range of values for k and c
k_values = np.linspace(1, 200, 50)  # Adjust as necessary
c_values = np.linspace(1, 50, 50)  # Adjust as necessary

# Storage for results
results = np.zeros((len(k_values), len(c_values)))

# Simulate for each combination of k and c
for i, k in enumerate(k_values):
    for j, c in enumerate(c_values):
        solution = odeint(system_derivatives, initial_conditions, t, args=(m, c, k))
        v = solution[:, 1]
        a = np.gradient(v, t)  # Acceleration
        max_accel = max(np.abs(a))
        
        # Store max acceleration in results
        results[i, j] = max_accel

# Create a custom colormap for the heatmap
colors = [(0, 1, 0), (1, 1, 0), (1, 0, 0)]  # Green -> Yellow -> Red
cmap_name = 'green_yellow_red'
cm = mcolors.LinearSegmentedColormap.from_list(cmap_name, colors, N=100)

# Plot the heatmap
fig, ax = plt.subplots(figsize=(10, 8))
cax = ax.imshow(results, extent=[c_values.min(), c_values.max(), k_values.min(), k_values.max()], 
           aspect='auto', origin='lower', cmap=cm, vmin=0, vmax=max_allowable_accel)

# Add a contour to indicate where max acceleration is hit
contour = ax.contour(c_values, k_values, results, levels=[max_allowable_accel], colors='black')
plt.colorbar(cax, label='Max Acceleration (m/s^2)')

ax.set_xlabel('Damping Coefficient c (kg/s)')
ax.set_ylabel('Spring Constant k (N/m)')
ax.set_title('Achievable Max Acceleration for k and c values')
plt.show()
