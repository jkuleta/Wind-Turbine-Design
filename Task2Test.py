# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.special import gamma


# Load the datasets
df_5MW = pd.read_csv('5MW WT Power Curve.csv')
df_3_5MW = pd.read_csv('3.5MW WT Power Curve scaled.csv')


D_ref = 126 # meter - Rotor diameter of reference turbine
H_ref = 90 # meter - Hub height of reference turbine
P_ref = 5000 # kW - Rated power of reference turbine

P_rated = 3500 # kW - Rated power of scaled turbine
D_scale = D_ref * (P_rated/P_ref)**(1/2)

v_cutin = 3 # m/s - Cut-in wind speed
v_cutout = 25 # m/s - Cut-out wind speed
v_rated = 11.4 # m/s - Rated wind speed


Cp_ref = 0.482 # Reference turbine power coefficient




#Weibull parameters
k = 2.241  # Shape parameter found by Marcos
A = 8.97   # Scale parameter found by Marcos

rho = 1.225 # kg/m^3 - Air density






# Define the cost function
def calculate_onshore_cost(D, D_scale):
    return 0.70 + 0.30 * (D / D_scale) ** 2.6

# Define the power curve function
def power_curve(v, v_cutin, v_rated, v_cutout, P_rated, D):
    if v < v_cutin or v > v_cutout:
        return 0
    elif v_cutin <= v and 0.5 * rho * np.pi * (D / 2) ** 2 * Cp_ref * v ** 3 / 1000 < P_rated:
        power = 0.5 * rho * np.pi * (D / 2) ** 2 * Cp_ref * v ** 3 / 1000
        return min(power, P_rated)
    else:
        return P_rated

# Define the Weibull probability density function
def weibull_pdf(v, A, k):
    return (k / A) * (v / A)**(k - 1) * np.exp(-(v / A)**k)


def calculate_AEP(power_curve, pdf_values, hours_per_year=8760, delta_v=0.1):
    AEP = np.sum([p * pdf * hours_per_year * delta_v for p, pdf in zip(power_curve, pdf_values)])
    return AEP / 1e6  # Convert to GWh

def calculate_LPC(C,AEP):
    return C/AEP*1000









# %%
# Range of wind speeds
wind_speeds = np.arange(0, 26, 0.1)

# Initialize lists to store results
diameters = np.arange(D_scale - 10, D_scale + 31, 1)
LPC_values = []
AEP_values = []

plt.figure(figsize=(10, 5))

# Loop over each diameter
for D in diameters:
    # Calculate Power Curve
    power_output = [power_curve(v, v_cutin, v_rated, v_cutout, P_rated, D) for v in wind_speeds]

    # Calculate Weibull PDF 
    pdf_values = weibull_pdf(wind_speeds, A, k)

    # Calculate Annual Energy Production (AEP)
    AEP = calculate_AEP(power_output, pdf_values)
    AEP_values.append(AEP)
    print(f"Estimated Annual Energy Production (AEP) for D={D:.2f}m: {AEP:.2f} GWh")

    # Calculate Levelized Cost of Energy (LPC)
    C = calculate_onshore_cost(D, D_scale)
    LPC = calculate_LPC(C, AEP)
    LPC_values.append(LPC)
    print(f"Levelized Cost of Energy (LPC) for D={D:.2f}m: {LPC:.2f} $/MWh")

    # Plot the power curve for the current diameter
    plt.plot(wind_speeds, power_output, label=f'D={D:.1f}m', color=plt.cm.viridis((D - diameters[0]) / (diameters[-1] - diameters[0])))

# Finalize the power curve plot
plt.xlabel('Wind Speed (m/s)')
plt.ylabel('Power Output (kW)')
plt.title('Wind Turbine Power Curves for Different Diameters')
plt.xlim(2.5, 25)
plt.ylim(0, 3700)
plt.xticks(np.arange(3, 26, 1))
plt.axvline(x=v_rated, color='r', linestyle='--', label='Rated Wind Speed')
plt.plot(df_3_5MW.iloc[:, 0], df_3_5MW.iloc[:, 1], label='3.5MW Scaled Turbine', color='black', linestyle='-', linewidth=3)
plt.legend(bbox_to_anchor=(1.03, 1.075), loc='upper left')
plt.grid(True)
plt.show()








# Find the optimum diameter based on the minimum LPC
optimum_diameter_index = np.argmin(LPC_values)
optimum_diameter = diameters[optimum_diameter_index]
optimum_LPC = LPC_values[optimum_diameter_index]

print(f"The optimum rotor diameter is {optimum_diameter:.2f} meters with a minimum LPC of {optimum_LPC:.2f} $/MWh")
# Combined plot for LPC and AEP vs Rotor Diameter
fig, ax1 = plt.subplots(figsize=(10, 5))

# Plot LPC
color = 'tab:blue'
ax1.set_xlabel('Rotor Diameter (m)')
ax1.set_ylabel('Levelized Cost of Energy (LPC) ($/MWh)', color=color)
ax1.plot(diameters, LPC_values, marker='o', color=color, label='LPC')
ax1.tick_params(axis='y', labelcolor=color)

# Create a second y-axis for AEP
ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Annual Energy Production (AEP) (GWh)', color=color)
ax2.plot(diameters, AEP_values, marker='o', color=color, label='AEP')
ax2.tick_params(axis='y', labelcolor=color)

# Plot vertical line at optimum diameter
ax1.axvline(x=optimum_diameter, color='green', linestyle='--', label=f'Optimum Diameter: {optimum_diameter:.2f}m')

# Add title and grid
fig.suptitle('LPC and AEP vs Rotor Diameter')
fig.tight_layout()
ax1.grid(True)

# Show plot
plt.show()

