import matplotlib.pyplot as plt
import numpy as np

D = 105  # Rotor diameter
TSR = 8  # Tip-speed ratio
V_in = 3
V_out = 25
V_rated = 11.4
P_rated = 3.5e6

R = D / 2  # Rotor radius
V = np.arange(V_in, V_out, 0.1)  # Wind speed range

# Calculate omega (rotational speed in rad/s)
omega = np.where(V < V_rated, TSR * V / R, TSR * V_rated / R)

# Convert omega to RPM
omega_RPM = omega * 60 / (2 * np.pi)

#tip speed
V_tip = omega[-1] * R
print("Tip speed [m/s]:",V_tip)

#print rotational speed range
print("Rotational speed range - min:", omega_RPM[0], ", max:", omega_RPM[-1])

#torque in the shaft
torque = P_rated / omega[-1]
print("Torque [Nm]:", torque)

# Plot RPM vs wind speed
plt.plot(V, omega_RPM, label="Rotor Speed (RPM)")
plt.xlabel("Wind Speed (m/s)")
plt.ylabel("Rotational Speed (RPM)")
plt.title("Rotor Speed vs Wind Speed")
plt.legend()
plt.grid()
plt.show()
