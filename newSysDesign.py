"""
System design, simulation and optimization program for GISMO payload
Specifications:
 - Maximum G Force Experienced and/or Maximum Kinetic Energy
 - Maximum Displacement (Room for mass to move within the spring damper system)
 - Thrust 
 - c and K values for SMD system
 - Mass of payload
 - Mass of STEMnaut capsule
 - Drop height
 - Initial Velocity
 - Impact Velocity
 - Drag Coefficient of Nose Cone


 A successful design will include:
 - Maximum G Force under threshold
 - Displacement under threshold

 Deliverables:
 - Plot of Velocity (x) against Height (y)


 Base Equations and Relations

"""
from scipy.optimize import minimize
import numpy as np
import matplotlib.pyplot as plt

mass = 0.2  # kg of STEMnaut capsule
initial_position = 0  # m of smd system
#impact_velocity = 6  # m/s
time_step = 0.001  # Time step for simulation (s)
total_time = 3.0  # Total simulation time (s)
desired_max_acceleration = 120 #during/after impact
displacement_threshold = .17 # meters of displacement of the spring mass damper system in one direction
mass_kg = 3  # Mass in kilograms of whole payload
diameter_m = 0.127  # Diameter in meters
height_m = 130  # Initial height in meters
dt = 0.001  # Time step in seconds
initial_velocity_m_per_s = 4  # Initial velocity in m/s
F_thrust = 29.3  # Thrust force in Newtons

# Constants
g = 9.81  # Acceleration due to gravity in m/s^2
rho = 1.225  # Air density in kg/m^3
A = np.pi * (diameter_m / 2)**2  # Cross-sectional area in m^2
drag_coefficient = 0.3  # Drag coefficient for a sphere

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
impact_velocity = velocities[-1]



def simulate_system_with_params(c, K):
    time = 0.0
    position = initial_position
    velocity = impact_velocity
    acceleration_list = []  # To store acceleration values
    position_list = []      # To store position values

    while time < total_time:
        # Calculate acceleration (from Newton's second law)
        acceleration = (-c * velocity - K * position) / mass
        
        # Update velocity and position using the Euler method
        velocity += acceleration * time_step
        position += velocity * time_step

        # Store acceleration and position values
        acceleration_list.append(acceleration)
        position_list.append(position)

        # Update time
        time += time_step

    return position_list, acceleration_list 

# Define the objective function (e.g., a simple quadratic function)
def spring_mass_damper_simulation(x):
    # Initialize variables
    damping_coefficient = x[0]   # Ns/m
    spring_constant = x[1]       # N/m
    time = 0.0
    position = initial_position
    velocity = impact_velocity
    max_displacement = 0.0
    
    while time < total_time:
        # Calculate acceleration (from Newton's second law)
        acceleration = (-damping_coefficient * velocity - spring_constant * position) / mass
        
        # Update velocity and position using the Euler method
        velocity += acceleration * time_step
        position += velocity * time_step
        
        # Update time
        time += time_step
        
        # Update maximum displacement if needed
        max_displacement = max(max_displacement, abs(position))
    
    return np.abs(max_displacement)

def acceleration_constraint(x):
    damping_coefficient = x[0]
    spring_constant = x[1]
    time = 0.0
    position = initial_position
    velocity = impact_velocity
    max_acceleration = 0.0  # Initialize max acceleration

    while time < total_time:
        # Calculate acceleration (from Newton's second law)
        acceleration = (-damping_coefficient * velocity - spring_constant * position) / mass

        # Check for max acceleration
        max_acceleration = max(max_acceleration, abs(acceleration))

        # Update velocity and position using the Euler method
        velocity += acceleration * time_step
        position += velocity * time_step

        # Update time
        time += time_step

    # The constraint function should return a value less than or equal to zero when the constraint is met
    return desired_max_acceleration - max_acceleration

def spring_constant_constraint(x):
    spring_constant = x[1]
    K_min = 0.0328  # Adjust this to your minimum allowable spring constant
    K_max = 361.55  # Adjust this to your maximum allowable spring constant

    # The constraint function should return a value less than or equal to zero when the constraint is met
    return min(spring_constant - K_min, K_max - spring_constant)

# Define constraints
constraints = [{'type': 'ineq', 'fun': acceleration_constraint},
               {'type': 'ineq', 'fun': spring_constant_constraint}]



# Initial guess and bounds
initial_guess = [0.1, 10.0]  # Adjust these based on your knowledge
bounds = [(0, None), (0, None)]  # Non-negative values for damping and spring constant

# Choose an optimization method (e.g., SLSQP)
result = minimize(spring_mass_damper_simulation, initial_guess, method='SLSQP', bounds=bounds, constraints=constraints)



# Extract the results
optimized_params = result.x
minimum_value = result.fun
success = result.success

print("Optimized c:", optimized_params[0])
print("Optimized K:", optimized_params[1])
print("Minimum Value:", minimum_value)
print("Success:", success)

# Use the optimized c and K values
optimal_c = optimized_params[0]
optimal_K = optimized_params[1]

# Simulate the system with optimized c and K values
displacement, acceleration = simulate_system_with_params(optimal_c, optimal_K)

# Plot displacement vs. time
plt.figure(figsize=(10, 8))
plt.subplot(2, 2, 1)
time_values = np.arange(0, total_time + time_step, time_step)  # Include the endpoint
plt.plot(time_values, displacement)
plt.xlabel('Time (s)')
plt.ylabel('Displacement (m)')
plt.title('Displacement vs. Time')

# Plot acceleration vs. time
plt.subplot(2, 2, 3)
plt.plot(time_values, acceleration)
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (m/s^2)')
plt.title('Acceleration vs. Time')

# Plot velocity vs height - make this plot wider
plt.subplot(2, 2, (2, 4))  # This will span the plot across two columns
plt.plot(velocities, heights)
plt.xlabel('Velocity (m/s)')
plt.ylabel('Height (m)')
plt.title('Velocity vs. Height During Descent')
#plt.gca().invert_yaxis()  # Invert y-axis to show descent from initial height to ground
plt.grid(True)

plt.tight_layout()  # This will ensure the plots are not overlapping
plt.show()
