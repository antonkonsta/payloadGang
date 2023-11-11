'''
This module is used to model and store governing equations.

Since odeint library is used to solve the ODE's, equations are modeled as functions
in the syntax required by odeint. They are not standalone functions.
'''

# SPRING MASS DAMPER MODEL
def spring_mass_damper(initial_conditions, t, m_capsule, c, k):
    #print("Mass of capsule: ", m_capsule, c, k)
    x, v = initial_conditions
    dxdt = v
    dydt = (-k * x - c * v) / m_capsule
    return [dxdt, dydt]

def descent(y, t, rho, mass_payload, drag_coefficient, area, thrust):
    v, h = y  # Unpack the current values of velocity and height
    # Drag force: Fd = 1/2 * rho * v^2 * Cd * A
    F_drag = 0.5 * rho * abs(v) * v * drag_coefficient * area  # Abs(v) ensures correct direction of drag
    # Net force
    net_force = mass_payload * g - F_drag - thrust
    # Acceleration
    dvdt = net_force / mass
    # Derivative of height is the velocity
    dhdt = -v  # Negative because as the object falls, height decreases
    return [dvdt, dhdt]