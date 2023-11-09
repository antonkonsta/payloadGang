import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Differential equations for the spring-mass-damper system
def system_derivatives(y, t, m, c, k):
    x, v = y
    dxdt = v
    dvdt = (-c * v - k * x) / m + g  # adding gravity
    return [dxdt, dvdt]

# Known parameters
g = 9.81  # gravitational acceleration (m/s^2)
m = float(input("Enter the mass of the system (kg): "))  # mass of the system
v0 = float(input("Enter the initial velocity at impact (m/s): "))  # initial velocity
max_disp = float(input("Enter the max displacement (m): "))  # max allowable displacement

# Time array for simulation
t = np.linspace(0, 10, 1000)  # Adjust as necessary

# Initial conditions: [initial displacement, initial velocity]
initial_conditions = [0, v0]

# Input spring constant and damping coefficient
k = float(input("Enter the spring constant (N/m): "))
c = float(input("Enter the damping coefficient (kg/s): "))

# Solve the system
solution = odeint(system_derivatives, initial_conditions, t, args=(m, c, k))

# Extract displacement (x) and velocity (v)
x = solution[:, 0]
v = solution[:, 1]
a = np.gradient(v, t)  # Acceleration

# Plot the results
fig, ax = plt.subplots(3, 1, figsize=(10, 8))

ax[0].plot(t, x, label='Displacement (m)')
ax[0].axhline(y=max_disp, color='r', linestyle='--', label=f'Max Displacement = {max_disp}m')
#5ax[0].axhline(y=-max_disp, color='r', linestyle='--', label=f'Min Displacement = {-max_disp}m')
ax[0].set_title('Displacement vs Time')
ax[0].set_xlabel('Time (s)')
ax[0].set_ylabel('Displacement (m)')
ax[0].grid(True)
ax[0].legend()

ax[1].plot(t, v, label='Velocity (m/s)', color='g')
ax[1].set_title('Velocity vs Time')
ax[1].set_xlabel('Time (s)')    
ax[1].set_ylabel('Velocity (m/s)')
ax[1].grid(True)

ax[2].plot(t, a, label='Acceleration (m/s^2)', color='r')
ax[2].set_title('Acceleration vs Time')
ax[2].set_xlabel('Time (s)')
ax[2].set_ylabel('Acceleration (m/s^2)')
ax[2].grid(True)

plt.tight_layout()
plt.show()

# Check maximum acceleration
print(f"Maximum acceleration experienced: {max(np.abs(a))} m/s^2")
