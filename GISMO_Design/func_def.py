from scipy.integrate import odeint
from ODEs import spring_mass_damper, descent
import numpy as np

def simulate_smd(initial_displacement, initial_velocity, m_capsule, c, k, t):
    initial_conditions = [initial_displacement, initial_velocity]

    # Solve the system
    solution = odeint(spring_mass_damper, initial_conditions, t,args=(m_capsule, c, k))

    # Extract displacement (x) and velocity (v) and calculate acceleration
    displacement = solution[:, 0]
    velocity= solution[:, 1]
    acceleration = np.gradient(velocity, t)
    return displacement, velocity, acceleration

def simulate_descent(initial_state, t, args=(rho, mass, drag_coefficient, area, thrust)):
