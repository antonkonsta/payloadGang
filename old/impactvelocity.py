import math
import matplotlib.pyplot as plt

# Set up your variables here
mass_kg = 4.536  # Example value (10 lbs to kg), replace with your actual value
diameter_m = 0.127  # Example value (5 inches to meters), replace with your actual value
height_m = 130  # 800 ft = 243.84 m, 400 ft = 121.92 m
dt = 0.001  # Time step
initial_velocity_m_per_s = 3.9624 # Starting from rest; modify if different
F_thrust = 5

def impact_velocity(mass_kg, diameter_m, drag_coefficient, height_m, initial_velocity_m_per_s, F_thrust, dt=0.001):
    """Compute velocity upon impact of a nosecone (in SI units)."""
    
    g = 9.81  # acceleration due to gravity, m/s^2
    rho = 1.225  # air density, kg/m^3
    A = math.pi * (diameter_m/2)**2  # cross-sectional area, m^2
    
    velocity = initial_velocity_m_per_s
    while height_m > 0:
        F_gravity = mass_kg * g
        F_drag = 0.5 * drag_coefficient * rho * A * velocity**2
        net_force = F_gravity - F_drag - F_thrust
        
        # Compute acceleration
        acceleration = net_force / mass_kg
        
        # Update velocity and height
        velocity += acceleration * dt
        height_m -= velocity * dt
        
    return velocity

# Create a list of drag coefficients for the x-axis and compute the corresponding impact velocities
drag_coefficients = [i*0.01 for i in range(1, 101)]  # Example: values from 0.01 to 1.0 in steps of 0.01
impact_velocities = [impact_velocity(mass_kg, diameter_m, cd, height_m, initial_velocity_m_per_s, F_thrust, dt) for cd in drag_coefficients]

kinetic_energies = [0.5 * mass_kg * v**2 for v in impact_velocities]



# Set up side-by-side plots
plt.figure(figsize=(14, 6))

# Plot impact velocities
plt.subplot(1, 2, 1)
plt.plot(drag_coefficients, impact_velocities)
plt.xlabel('Drag Coefficient ($C_d$)')
plt.ylabel('Impact Velocity (m/s)')
plt.title('Impact Velocity vs. Drag Coefficient')
plt.grid(True)

# Plot kinetic energy
plt.subplot(1, 2, 2)
plt.plot(drag_coefficients, kinetic_energies)
plt.xlabel('Drag Coefficient ($C_d$)')
plt.ylabel('Kinetic Energy Upon Impact (Joules)')
plt.title('Kinetic Energy vs. Drag Coefficient')
plt.grid(True)

plt.tight_layout()  # Adjusts spacing between plots
plt.show()