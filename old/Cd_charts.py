import numpy as np
import matplotlib.pyplot as plt

# Constants and Parameters (SI Units)
g = 9.81  # Acceleration due to gravity (m/s^2)
rho = 1.225  # Air density (kg/m^3)
A = 0.0108528815  # Cross-sectional area of the nosecone (m^2)    
m = 4.536  # Mass of the nosecone (kg)wddwad

# Range of Cd values 
Cd_values = np.linspace(0.2, 0.4, 100)

# Calculate terminal velocity for each Cd value
terminal_velocities = np.sqrt((2 * m * g) / (rho * A * Cd_values))

# Calculate kinetic energy for each Cd value
kinetic_energies = 0.5 * m * terminal_velocities**2  

# Specific Cd values and their corresponding terminal velocities and kinetic energies
specific_Cd_values = [0.28, 0.35, 0.3088]  # Add the Cd values you want to highlight
specific_terminal_velocities = np.sqrt((2 * m * g) / (rho * A * np.array(specific_Cd_values)))
specific_kinetic_energies = 0.5 * m * specific_terminal_velocities**2

# Plot terminal velocity vs. Cd
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(Cd_values, terminal_velocities, label="Terminal Velocity vs Drag Coefficient")
plt.scatter(specific_Cd_values, specific_terminal_velocities, c='red', marker='o', label="Specific Cd Values", linestyle='dotted')
plt.title("Terminal Velocity vs Drag Coefficient")
plt.xlabel("Drag Coefficient (Cd)")
plt.ylabel("Terminal Velocity (m/s)")
plt.grid(True)
plt.legend()

# Annotate the points with (Cd, Velocity) values
for i, txt in enumerate(specific_Cd_values):
    plt.annotate(f"({txt:.2f}, {specific_terminal_velocities[i]:.2f} m/s)", (specific_Cd_values[i], specific_terminal_velocities[i]), textcoords="offset points", xytext=(0, 10), ha='center')

# Plot kinetic energy vs. Cd
plt.subplot(1, 2, 2)
plt.plot(Cd_values, kinetic_energies, label="Kinetic Energy vs Drag Coefficient")
plt.scatter(specific_Cd_values, specific_kinetic_energies, c='red', marker='o', label="Specific Cd Values", linestyle='dotted')
plt.title("Kinetic Energy vs Drag Coefficient")
plt.xlabel("Drag Coefficient (Cd)")
plt.ylabel("Kinetic Energy (Joules)")
plt.grid(True)
plt.legend()

# Annotate the points with (Cd, Kinetic Energy) values
for i, txt in enumerate(specific_Cd_values):
    plt.annotate(f"({txt:.2f}, {specific_kinetic_energies[i]:.2f} J)", (specific_Cd_values[i], specific_kinetic_energies[i]), textcoords="offset points", xytext=(0, 10), ha='center')

plt.tight_layout()
plt.show()
