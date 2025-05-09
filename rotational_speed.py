import matplotlib.pyplot as plt
import numpy as np

#Update global font size
plt.rcParams.update({'font.size': 14}) 

def average(x1, x2):
    return (x1 + x2) / 2

def weibull_pdf(V_o_range, A, k):
    return (k / A) * (V_o_range / A) ** (k - 1) * np.exp(- (V_o_range / A) ** k)

D = 118.4-3  # Rotor diameter (-hub diameter)
D_scale = 105.42-3 #Scaled diameter
TSR = 7  # Tip-speed ratio as the reference turbine
V_in = 3
V_out = 25
V_rated = 10.4
V_rated_scale = 11.4
P_rated = 3.5e6  # Rated power in watts
cp = 0.482

R = D / 2  # Rotor radius
R_scale = D_scale / 2
V = np.arange(V_in, V_out, 0.1)  # Wind speed range

# Calculate omega (rotational speed in rad/s)
omega = np.where(V < V_rated, TSR * V / R, TSR * V_rated / R)
omega_scale = np.where(V < V_rated_scale, TSR * V / R_scale, TSR * V_rated_scale / R_scale)

#calculate power
Power = np.where(V <= V_rated, cp*0.5*1.225*R**2*np.pi*V**3, P_rated)

# Convert omega to RPM
omega_RPM = omega * 60 / (2 * np.pi)
omega_RPM_scale = omega_scale * 60 /(2 * np.pi)

# Tip speed
V_tip = omega[-1] * R
print("Tip speed [m/s]:", V_tip)

# Print rotational speed range
print("Rotational speed range - min:", omega_RPM[0], ", max:", omega_RPM[-1])

# Torque in the shaft
torque = Power/ omega
print("Torque [MNm]:", max(torque/(10**6)))

plt.figure()
plt.plot(V, torque)
plt.grid()
plt.show()

print(P_rated/omega[-1])

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
plt.figure(figsize=(10,5))

for location, (A, k) in locations.items():
    weibull_dist = weibull_pdf(V, A, k)
    plt.plot(V, weibull_dist, alpha=0.65, linestyle = '--',label=f"{location} (A={A:.2f}, k={k:.2f})")  # Added A and k to the label

# Plot average Weibull distribution as a solid line
weibull_avg = weibull_pdf(V, A_avg, k_avg)
plt.plot(V, weibull_avg, color="black", linewidth=2, label=f"Average (A={A_avg:.2f}, k={k_avg:.2f})")

plt.xlabel("Wind Speed [m/s]")
plt.ylabel("Probability Density")
plt.legend()
plt.grid()

# Plot RPM vs Wind Speed
plt.figure(figsize=(10,5))
plt.plot(V, omega_RPM, label="Optimum diameter", linestyle='-', color = 'black')
plt.plot(V, omega_RPM_scale, label="Scaled diameter", linestyle='--', color='black')
plt.xlabel("Wind Speed [m/s]")
plt.ylabel("Rotational Speed [RPM]")
plt.legend()
plt.grid()

# Show all plots without requiring manual closure
plt.show(block=True)
