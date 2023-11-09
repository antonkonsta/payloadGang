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

mass = 0.1  # kg
initial_position = 0  # m
initial_velocity = 15  # m/s
time_step = 0.001  # Time step for simulation (s)
total_time = 3.0  # Total simulation time (s)
desired_acceleration = 120
displacement_threshold = 1

def simulate_system_with_params(c, K):
    time = 0.0
    position = initial_position
    velocity = initial_velocity
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
    spring_constant = x[1] # N/m
    time = 0.0
    position = initial_position
    velocity = initial_velocity
    max_acceleration = 0.0
    
    while time < total_time:
        # Calculate acceleration (from Newton's second law)
        acceleration = (-damping_coefficient * velocity - spring_constant * position) / mass
        
        # Update velocity and position using the Euler method
        velocity += acceleration * time_step
        position += velocity * time_step
        
        # Update time
        time += time_step
        
        # Update maximum acceleration if needed
        max_acceleration = max(max_acceleration, abs(acceleration))
    
    return np.abs((desired_acceleration - max_acceleration))

def displacement_constraint(x):
    damping_coefficient = x[0]
    spring_constant = x[1]
    
    time = 0.0
    position = initial_position
    velocity = initial_velocity

    while time < total_time:
        # Calculate acceleration (from Newton's second law)
        acceleration = (-damping_coefficient * velocity - spring_constant * position) / mass

        # Update velocity and position using the Euler method
        velocity += acceleration * time_step
        position += velocity * time_step

        # Update time
        time += time_step

    return position - displacement_threshold # Ensure position is below the threshold

# Define constraints
constraints = [{'type': 'eq', 'fun': displacement_constraint}]


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
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
time_values = np.arange(0, total_time + time_step, time_step)  # Include the endpoint
plt.plot(time_values, displacement)
plt.xlabel('Time (s)')
plt.ylabel('Displacement (m)')
plt.title('Displacement vs. Time')

# Plot acceleration vs. time
plt.subplot(1, 2, 2)
plt.plot(time_values, acceleration)
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (m/s^2)')
plt.title('Acceleration vs. Time')

plt.tight_layout()
plt.show()
