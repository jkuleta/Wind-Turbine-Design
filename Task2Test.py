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


# Mean wind speed (example value, replace with actual data)
mean_wind_speed = 8.0  # m/s
# Standard deviation of wind speed (example value, replace with actual data)
std_wind_speed = 2.5  # m/s

# Estimate Weibull parameters
k = (std_wind_speed / mean_wind_speed) ** -1.086
A = mean_wind_speed / gamma(1 + 1 / k)



# Define the cost function
def calculate_onshore_cost(D, D_scale):
    return 0.70 + 0.30 * (D / D_scale) ** 2.6

# Define the power curve function
def power_curve(v, v_cutin, v_rated, v_cutout, P_rated):
    if v < v_cutin or v > v_cutout:
        return 0
    elif v_cutin <= v < v_rated:
        return P_rated * ((v - v_cutin) / (v_rated - v_cutin)) ** 2
    else:
        return P_rated

# Define the Weibull probability density function
def weibull_pdf(v, A, k):
    return (k / A) * (v / A)**(k - 1) * np.exp(-(v / A)**k)








# Calculate power curve for a range of wind speeds
wind_speeds = np.arange(0, 26, 0.1)
power_output = [power_curve(v, v_cutin, v_rated, v_cutout, P_rated) for v in wind_speeds]

# Plot the power curves
plt.figure(figsize=(10, 5))
plt.plot(df_3_5MW.iloc[:, 0], df_3_5MW.iloc[:, 1], label='3.5MW Scaled Turbine')
plt.plot(wind_speeds, power_output, label='Calculated 3.5MW Power Curve', linestyle='--')
plt.xlabel('Wind Speed (m/s)')
plt.ylabel('Power Output (kW)')
plt.title('Wind Turbine Power Curves')
plt.xlim(3, 25.5)
plt.ylim(0, 3700)
plt.xticks(np.arange(3, 26, 1))
plt.axvline(x=v_rated, color='r', linestyle='--', label='Rated Wind Speed')
plt.legend()
plt.grid(True)
plt.show()



# Calculate Weibull PDF for each wind speed
pdf_values = weibull_pdf(wind_speeds, A, k)

# Calculate Annual Energy Production (AEP)
hours_per_year = 8760
delta_v = 0.1  # Wind speed step (m/s)
AEP = np.sum([p * pdf * hours_per_year * delta_v for p, pdf in zip(power_output, pdf_values)])

print(f"Estimated Annual Energy Production (AEP): {AEP / 1e6:.2f} GWh")







































