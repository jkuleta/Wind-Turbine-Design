import matplotlib.pyplot as plt
import numpy as np

def average(x1, x2):
    return (x1 + x2) / 2

def weibull_pdf(V_o_range, A, k):
    return (k / A) * (V_o_range / A) ** (k - 1) * np.exp(- (V_o_range / A) ** k)

D = 118.4-3  # Rotor diameter
TSR = 8  # Tip-speed ratio
V_in = 3
V_out = 25
V_rated = 11.4
P_rated = 3.5e6  # Rated power in watts

R = D / 2  # Rotor radius
V = np.arange(V_in, V_out, 0.1)  # Wind speed range

# Calculate omega (rotational speed in rad/s)
omega = np.where(V < V_rated, TSR * V / R, TSR * V_rated / R)

# Convert omega to RPM
omega_RPM = omega * 60 / (2 * np.pi)

# Tip speed
V_tip = omega[-1] * R
print("Tip speed [m/s]:", V_tip)

# Print rotational speed range
print("Rotational speed range - min:", omega_RPM[0], ", max:", omega_RPM[-1])

# Torque in the shaft
torque = P_rated / omega[-1]
print("Torque [Nm]:", torque)

# Weibull parameters for different locations
locations = {
    "Netherlands": (average(7.9, 9.3), average(2.05, 2.46)),
    "Scotland": (average(8.4, 9.9), average(1.94, 2.29)),
    "Bornholm": (average(8.3, 9.8), average(2.02, 2.4)),
    "Poland": (average(8.2, 9.7), average(2.1, 2.5)),
    "Germany": (average(8.4, 9.8), average(2.14, 2.51)),
}

# Compute average A and k
A_values = [A for A, k in locations.values()]
k_values = [k for A, k in locations.values()]
A_avg = np.mean(A_values)
k_avg = np.mean(k_values)

# Compute and plot Weibull distributions
plt.figure(figsize=(8, 6))

for location, (A, k) in locations.items():
    weibull_dist = weibull_pdf(V, A, k)
    plt.plot(V, weibull_dist, alpha=0.65, label=f"{location}")  # Shaded distributions

# Plot average Weibull distribution as a solid line
weibull_avg = weibull_pdf(V, A_avg, k_avg)
plt.plot(V, weibull_avg, color="black", linewidth=2, label="Average")

plt.xlabel("Wind Speed (m/s)")
plt.ylabel("Probability Density")
plt.title("Weibull Wind Speed Distributions")
plt.legend()
plt.grid()

# Plot RPM vs Wind Speed
plt.figure(figsize=(8, 6))
plt.plot(V, omega_RPM, label="Rotor Speed (RPM)")
plt.xlabel("Wind Speed (m/s)")
plt.ylabel("Rotational Speed (RPM)")
plt.title("Rotor Speed vs Wind Speed")
plt.legend()
plt.grid()

# Show all plots without requiring manual closure
plt.show(block=True)
