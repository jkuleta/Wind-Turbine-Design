import matplotlib.pyplot as plt
import numpy as np


#Update global font size
plt.rcParams.update({'font.size': 14}) 

#Turbine modelling
R = (118-3)/2 # Rotor radius 
TSR = 7.6  # Tip-speed ratio as the reference turbine
V_in = 3
V_out = 25
V_rated = 10.4
P_rated = 3.5e6  # Rated power in watts
cp = 0.482

V = np.arange(V_in, V_out, 0.01)  # Wind speed range
omega = np.where(V <= V_rated, TSR * V / R, TSR * V_rated / R)
Power = np.where(V <= V_rated, cp*0.5*1.225*R**2*np.pi*V**3, P_rated)
omega_RPM = omega * 60 / (2 * np.pi)

#Gearbox modelling
gearbox_loss_percentage = 0.03 
gearbox_loss = gearbox_loss_percentage * P_rated * omega/omega[-1]  
gearbox_loss_rated = gearbox_loss_percentage * P_rated * omega[-1]/omega[-1] 
Power_gearbox_rated = P_rated - gearbox_loss_rated
Power_gearbox = Power - gearbox_loss
print(Power_gearbox)
#Generator modelling for symbols look at Henk Pollinder generator modelling chapter
Rs = 26e-3
Rr = 35e-3
Lm = 99e-3
Ls_sigma = 0.99e-3
Lr_sigma = 1.2e-3

Power_generator = Power_gearbox * 0.982 #Where did we find this number
Generator_loss = Power_gearbox - Power_generator

mu0 = 1.256e-6
l_s = 0.75
r_s = 0.42
p = 3
k_w = 0.85
N_s = 20
g = 4e-3

L_sm = 6*mu0*l_s*r_s*(k_w*N_s)**2/(p**2*g*np.pi)


Ls = Ls_sigma + L_sm
R_R = Rr * Ls**2/(L_sm**2)
Ll = (Ls_sigma + Ls)/L_sm + (Lr_sigma * Ls**2)/L_sm**2

#cable modelling
r_copper = 2.82e-8
A_cable = 3*400e-6
l_cable = 90
R_cable = r_copper * l_cable / A_cable
V_cable = 690
print(690)
I_cable = Power_generator / V_cable
print(I_cable)
print(R_cable)
Cable_loss = I_cable**2 * R_cable   
Power_cable = Power_generator - Cable_loss

print(r"Cable:",Power_cable/Power_generator)

#converter modelling
current_ratio = 0.4
converter_loss_percentage = 0.03
Power_in_converter = Power_cable
converter_loss = converter_loss_percentage * Power_in_converter 
converter_loss_actual = converter_loss * (1+10*current_ratio + 5*current_ratio**2+10*current_ratio+5*current_ratio**2)/31


#plotting

gearbox_loss = gearbox_loss/1000
converter_loss_actual = converter_loss_actual/1000
Generator_loss = Generator_loss/1000
Cable_loss = Cable_loss/1000
plt.figure(figsize=(10,5))
plt.plot(V, gearbox_loss,label = "Gearbox")
plt.plot(V, converter_loss_actual, label="Converter")
plt.plot(V, Generator_loss, label = 'Generator')
plt.plot(V, Cable_loss, label='Cable')
plt.xlabel(r'Wind speed $V$ [m/s]')
plt.ylabel("Power loss [kW]")
plt.legend()
plt.grid()
plt.show(block = False)

Power = Power/1000
Power_loss = gearbox_loss+converter_loss_actual+Generator_loss+Cable_loss
Power_to_grid = Power- gearbox_loss - converter_loss_actual - Generator_loss - Cable_loss

plt.figure(figsize=(10,5))
plt.plot(V, Power, label = "Power from the rotor")
plt.plot(V, Power_loss, label="Power loss")
plt.plot(V, Power_to_grid, label="Power to grid")
plt.xlabel(r'Wind speed $V$ [m/s]')
plt.ylabel("Power loss [kW]")
plt.legend()
plt.grid()
plt.show(block = False)

efficiency = Power_to_grid/Power

plt.figure(figsize=(10,5))
plt.plot(V, efficiency)
plt.xlabel(r'Wind speed $V$ [m/s]')
plt.ylabel("Efficiency")
plt.grid()
plt.show(block = True)

print(r'efficiency:', efficiency[-1])