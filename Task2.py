#%%############################################################################
###------------------------ Importing Libraries ----------------------------###
###############################################################################
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.special import gamma



# Load the datasets
df_5MW = pd.read_csv('5MW WT Power Curve.csv')
df_3_5MW = pd.read_csv('3.5MW WT Power Curve scaled.csv')

# Constants
D_ref = 126 # meter - Rotor diameter of reference turbine
H_ref = 90 # meter - Hub height of reference turbine
P_ref = 5000 # kW - Rated power of reference turbine
P_rated = 3500 # kW - Rated power of scaled turbine
D_scale = D_ref * (P_rated/P_ref)**(1/2)
v_cutin = 3 # m/s - Cut-in wind speed
v_cutout = 25 # m/s - Cut-out wind speed
v_rated = 11.4 # m/s - Rated wind speed
Cp_ref = 0.482 # Reference turbine power coefficient
k = 2.241  # Shape parameter found by Marcos
A = 8.97   # Scale parameter found by Marcos
rho = 1.225 # kg/m^3 - Air density





#%%############################################################################
###------------------------ Function Definitions ---------------------------###
###############################################################################

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


# Calculate Annual Energy Production (AEP)
def calculate_AEP(power_curve, pdf_values, hours_per_year=8760, delta_v=0.1):
    AEP = np.sum([p * pdf * hours_per_year * delta_v for p, pdf in zip(power_curve, pdf_values)])
    return AEP / 1e6  # Convert to GWh


# Calculate Levelized Cost of Energy (LPC)
def calculate_LPC(C, AEP):
    return C/AEP*1000













#%%############################################################################
###------------------------ Main Code --------------------------------------###
###############################################################################

# Define the range of wind speeds
wind_speeds = np.arange(0, 26, 0.1)

# Initialize lists to store results
diameters = np.arange(D_scale - 20, D_scale + 31, 1)
LPC_values = []
AEP_values = []







############## POWER CURVE ##############

# Plot and calculate the power curves for different rotor diameters
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
    print(f"Estimated AEP for D={D:.2f}m: {AEP:.2f} GWh")

    # Calculate Levelized Cost of Energy (LPC)
    C = calculate_onshore_cost(D, D_scale)
    LPC = calculate_LPC(C, AEP)
    LPC_values.append(LPC)
    print(f"LPC for D={D:.2f}m: {LPC:.2f} $/MWh \n")

    # Plot the power curve for the current diameter
    plt.plot(wind_speeds, power_output, color=plt.cm.turbo((D - diameters[0]) / (diameters[-1] - diameters[0])))

# Find the optimum diameter based on the minimum LPC
optimum_diameter_index = np.argmin(LPC_values)
optimum_diameter = diameters[optimum_diameter_index]
optimum_LPC = LPC_values[optimum_diameter_index]
print(f"The optimum rotor diameter is {optimum_diameter:.2f} meters with a minimum LPC of {optimum_LPC:.2f} $/MWh")


# Plot the power curve for the optimum diameter
optimum_power_output = [power_curve(v, v_cutin, v_rated, v_cutout, P_rated, optimum_diameter) for v in wind_speeds]
plt.plot(wind_speeds, optimum_power_output, label=f'Optimum D={optimum_diameter:.1f}m', color='black', linestyle='--', linewidth=2)
# Plot the power curve for the 3.5MW scaled turbine
plt.plot(df_3_5MW.iloc[:, 0], df_3_5MW.iloc[:, 1], label='5MW Turbine (scaled)', color='black', linestyle='-', linewidth=3)
# Finalize the power curve plot
plt.xlabel('Wind Speed [m/s]', fontsize=14)
plt.ylabel('Power Output [kW]', fontsize=14)
plt.title('Wind Turbine Power Curves for Different Diameters', fontsize=14)
plt.xlim(2.5, 25)
plt.ylim(0, 3700)
plt.xticks(np.arange(3, 26, 1))
plt.axvline(x=v_rated, color='grey', linestyle=':', label=f'5MW $v_{{rated}}$ = {v_rated} m/s')
plt.legend(loc='lower right', fontsize=12)
plt.grid(True)
# Add colorbar
sm = plt.cm.ScalarMappable(cmap='turbo', norm=plt.Normalize(vmin=diameters[0],vmax=diameters[-1]))
sm.set_array([])
cbar = plt.colorbar(sm, pad=0.02)
cbar.set_label('Rotor Diameter [m]',labelpad=-15, fontsize=14)
cbar.set_ticks([diameters[0], diameters[-1]])
cbar.set_ticklabels([f'{diameters[0]:.1f}m', f'{diameters[-1]:.1f}m'])
plt.show()








############## AEP AND LPC ##############

# Combined plot for LPC and AEP vs Rotor Diameter
fig, ax1 = plt.subplots(figsize=(10, 5))

# Plot LPC And AEP
color = 'tab:blue'
ax1.set_xlabel('Rotor Diameter [m]', fontsize=14)
ax1.set_ylabel('LPC [$/MWh]', color=color, fontsize=16)
ax1.plot(diameters, LPC_values, marker='o', color=color, label='LPC')
ax1.tick_params(axis='y', labelcolor=color, labelsize=14)
ax1.tick_params(axis='x', labelsize=14)
ax1.set_xticks(np.arange(85, 136, 5))

# Create a second y-axis for AEP
ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('AEP [GWh]', color=color, fontsize=14)
ax2.plot(diameters, AEP_values, marker='s', color=color, label='AEP')
ax2.tick_params(axis='y', labelcolor=color, labelsize=14)

# Plot vertical line at optimum diameter
ax1.axvline(x=optimum_diameter, color='green', linestyle='--', label=f'Optimum Diameter: {optimum_diameter:.1f}m')

# Add title and grid
fig.suptitle('Levelized Cost of Energy (LPC) and Annual Energy Production (AEP) vs Rotor Diameter', fontsize=14)
fig.tight_layout()
ax1.grid(True)
fig.legend(loc='upper center', bbox_to_anchor=(0.5, 0.02), ncol=3, fontsize=14)

# Show plot
plt.show()
