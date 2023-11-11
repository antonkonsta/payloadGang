from func_def import simulate_smd, simulate_descent
import ODEs as m 
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize


#============================== USER SETTINGS ============================== 
# Descent settings
deployment_height_ft = 450 # Feet
initial_deployment_velocity_fts = 13 # Feet/s
mass_payload_lb = 6.61 # Pounds
simulation_duration_d = 40# Seconds

# Nosecone info
drag_coefficient = 0.3
area_in = 16.82 # Inches Squared (Cross sectional area of payload)

# Spring Mass Damper settings
mass_capsule_lb = 0.5 # lbs
initial_displacement_in = 0 # inches
max_displacement_in = 5 # inches
simulation_duration_smd = 1# Seconds

#Simulation Setup:  (To "plug in" values of K, c or thrust, simply set the max & min to that value)
min_k = 0.001 # Minimum K Value
max_k = 999 # Maximum K Value

min_c = 0.001 # Minimum c Value
max_c = 99# Maximum c Value

min_thrust = 0 # Minimum Thrust (Newtons)
max_thrust = mass_payload_lb  * 4.44822 * .999 # Max Thrust (Newtons) - ( "mass_payload_lb  * 4.44822 * .99 " is used to ensure the force of thrust wont be above the weight of the payload)



#============================== VARIABLE SETUP (IGNORE) ============================== 

# Miscellaneous Constants
g = 9.81 # Gravity
rho = 1.225 # Air density in kg/m^3
data_points = 1000 # Number of data points to be taken

# Convert to SI units
deployment_height_m = deployment_height_ft * 0.3048
initial_deployment_velocity_ms = initial_deployment_velocity_fts* 0.3048
mass_payload_kg = mass_payload_lb * 0.45359237
mass_capsule_kg = mass_capsule_lb * 0.45359237
initial_displacement_m = initial_displacement_in * 0.0254
max_displacement_m = max_displacement_in * 0.0254
area_m = area_in * 0.00064516

# Array of time points for simulations
t_smd = np.linspace(0, simulation_duration_smd, data_points)
t_d = np.linspace(0, simulation_duration_d, data_points)



#============================== OPTIMIZATION FUNCTION ============================== 

def objective_function(params):
    k, c, thrust = params

    # Simulate the descent with the given thrust
    height, velocity_descent, acceleration_descent = simulate_descent(initial_deployment_velocity_ms, deployment_height_m, rho, mass_payload_kg, drag_coefficient, area_m, thrust, t_d)

    # Find impact velocity
    impact_velocity = velocity_descent[(np.abs(height)).argmin()]

    # Simulate the spring-mass-damper system with the impact velocity
    displacement, _, acceleration = simulate_smd(initial_displacement_m, impact_velocity, mass_capsule_kg, c, k, t_smd)

    # Calculate the max g-force and the displacement error (target - actual)
    max_g_force = np.max(np.abs(acceleration)) / g
    displacement_error = np.abs(max_displacement_in - (max(displacement) - min(displacement)) * 39.3701)  # Convert meters to inches

    # You can adjust the weights as per your preference
    return displacement_error + .4 * max_g_force

# Bounds for k, c, and thrust (assuming some reasonable bounds)
bounds = [(min_k, max_k), (min_c, max_c), (min_thrust, max_thrust)]

# Initial guesses for k, c, and thrust
initial_guess = [50, 5, 20]

# Perform the optimization
result = minimize(objective_function, initial_guess, bounds=bounds)



#============================== EXTRACT & CONVERT RESULTING DATA ============================== 

# Extract the optimized parameters
optimized_k, optimized_c, optimized_thrust = result.x

height, velocity_descent, acceleration_descent = simulate_descent(initial_deployment_velocity_ms, deployment_height_m, rho, mass_payload_kg, drag_coefficient, area_m, optimized_thrust, t_d)
# Find the index where height is closest to zero
zero_height_index = (np.abs(height)).argmin()

# Corresponding velocity at the point where height is closest to zero
impact_velocity = velocity_descent[zero_height_index]

displacement, velocity, acceleration = simulate_smd(initial_displacement_m, impact_velocity, mass_capsule_kg, optimized_c, optimized_k, t_smd)

# Convert units back to imperial
displacement_result = displacement  * 39.3701 
velocity_result = velocity * 3.28084
G_Force_result = acceleration * 0.101972
height_result = height * 3.28084
velocity_descent_result = velocity_descent * 3.28084


# Find the index of maximum magnitude in G Force and displacement
max_g_force_index = np.argmax(np.abs(G_Force_result))
max_displacement_index = np.argmax(np.abs(displacement_result))
min_displacement_index = np.argmin(displacement_result)
min_displacement = displacement_result[min_displacement_index]


# Maximum magnitude values for G Force and displacement
max_g_force = G_Force_result[max_g_force_index]
max_displacement = displacement_result[max_displacement_index]
total_displacement_difference = max_displacement - min_displacement

# Find the index where height is closest to zero
zero_height_index = (np.abs(height_result)).argmin()

# Corresponding velocity at the point where height is closest to zero
velocity_at_zero_height = velocity_descent_result[zero_height_index]



#============================== PLOTS ============================== 

# Font size for the text labels
label_fontsize = 13  # You can adjust this value as needed

# Plotting code
plt.figure(figsize=(10, 8))

# Displacement vs. Time
plt.subplot(2, 2, 1)
plt.plot(t_smd, displacement_result)
plt.scatter(t_smd[max_displacement_index], max_displacement, color='red')  # Mark the max point
plt.text(t_smd[max_displacement_index], max_displacement, f'  {max_displacement:.2f} in', color='black', fontsize=label_fontsize)  # Label the max point
plt.scatter(t_smd[min_displacement_index], min_displacement, color='blue')  # Mark the min point
plt.text(t_smd[min_displacement_index], min_displacement, f'  {min_displacement:.2f} in', color='black', fontsize=label_fontsize)  # Label the min point
plt.text(0.5 * (t_smd[-1] - t_smd[0]), 0.5 * (max_displacement + min_displacement), f'Total Displacement: {total_displacement_difference:.2f} in', horizontalalignment='center', color='black', fontsize=label_fontsize)
plt.xlabel('Time (s)')
plt.ylabel('Displacement (in)')
plt.title('Displacement vs. Time')
plt.grid(True)

# G Force vs. Time
plt.subplot(2, 2, 3)
plt.plot(t_smd, G_Force_result)
plt.scatter(t_smd[max_g_force_index], max_g_force, color='red')  # Mark the point
plt.text(t_smd[max_g_force_index], max_g_force, f'  {max_g_force:.2f} Gs', color='black', fontsize=label_fontsize)  # Label the point with increased font size
plt.xlabel('Time (s)')
plt.ylabel('G Force')
plt.title('G Force vs. Time')
plt.grid(True)

# Velocity vs. Height During Descent
plt.subplot(2, 2, 2)
plt.plot(velocity_descent_result, height_result)
# Mark the point
plt.scatter(velocity_at_zero_height, height_result[zero_height_index], color='red')  
# Label the point with increased font size and offset
plt.text(velocity_at_zero_height, height_result[zero_height_index] + 5, f'  {velocity_at_zero_height:.2f} ft/s', color='black', fontsize=label_fontsize)  
plt.axhline(y=deployment_height_ft, color='b', linestyle='--', label=f'Initial Height: {deployment_height_ft} ft')  # Dotted line for initial height
plt.axhline(y=0, color='darkgreen', linestyle='-', linewidth=2, label='Ground Level')  # Thick dark green line for ground level
plt.xlabel('Velocity (ft/s)')
plt.ylabel('Height (ft)')
plt.title('Velocity vs. Height During Descent')
plt.grid(True)

# Optimized Values Display
plt.subplot(2, 2, 4)
plt.axis('off')

# The y-coordinates are set to spread the text out within the subplot using normalized figure coordinates
plt.text(.55, 0.43, f'Simulation was ran with following values:', ha='left', fontsize=label_fontsize, transform=plt.gcf().transFigure)
plt.text(.58, 0.39, f'Desired Displacement: {max_displacement_in:.2f} in', ha='left', fontsize=11, transform=plt.gcf().transFigure)
plt.text(0.58, 0.36, f'Deployment Height:  {deployment_height_ft:.2f} ft', ha='left', fontsize=11, transform=plt.gcf().transFigure)
plt.text(0.58, 0.33, f'Initial Velocity: {initial_deployment_velocity_fts:.2f} ft/s', ha='left', fontsize=11, transform=plt.gcf().transFigure)
plt.text(0.58, 0.3, f'Total Payload Mass: {mass_payload_lb:.2f} lbs', ha='left', fontsize=11, transform=plt.gcf().transFigure)
plt.text(0.58, 0.27, f'STEMnaut Capsule Mass: {mass_capsule_lb:.2f} lbs', ha='left', fontsize=11, transform=plt.gcf().transFigure)

plt.text(.55, 0.2, f'Optimized Results:', ha='left', fontsize=label_fontsize, transform=plt.gcf().transFigure)
plt.text(.58, 0.16, f'Optimal Spring Constant (k): {optimized_k:.2f} N/m', ha='left', fontsize=11, transform=plt.gcf().transFigure)
plt.text(0.58, 0.13, f'Optimal Damping Coefficient (c): {optimized_c:.2f} Ns/m', ha='left', fontsize=11, transform=plt.gcf().transFigure)
plt.text(0.58, 0.1, f'Optimal Thrust: {optimized_thrust:.2f} N', ha='left', fontsize=11, transform=plt.gcf().transFigure)

# Set the x and y axis limits
plt.xlim(0, velocity_at_zero_height * 1.5)  # Adjust the right limit to be slightly more than the velocity at zero height
upper_limit = deployment_height_ft * 1.1  # Set upper limit to 110% of initial height
plt.ylim(-20, upper_limit)  # Adjust the lower limit to be slightly below zero, and set upper limit with buffer


print(f"Optimized Spring Constant (k): {optimized_k} N/m")
print(f"Optimized Damping Coefficient (c): {optimized_c} Ns/m")
print(f"Optimized Thrust: {optimized_thrust} N")

# Convert the impact velocity to feet per second for printing
impact_velocity_fts = impact_velocity * 3.28084  # Convert from m/s to ft/s

# Print the maximum g-force, the maximum displacement in inches, and the impact velocity in ft/s
print(f"Maximum G-Force Experienced: {max_g_force:.2f} Gs")
print(f"Maximum Displacement: {max_displacement:.2f} inches")
print(f"Impact Velocity: {impact_velocity_fts:.2f} ft/s")

plt.legend()
plt.tight_layout()
plt.show()
