clc; clear; close all;


%% Fixed parameters
lambda_design = 7; 
B = 3; 
r_R = linspace(0, 1, 100);  
sclaing_factor =(117.5/126);

%% Reference trubine

%- 1 = analytical
R_1 = 63;
alpha_airfoils_1 = {0, 0, 6, 6, 7.5, 5, 3.5, 5};
cl_airfoils_1 = {0, 0, 0.967, 0.967, 1.256, 1.062, 0.948, 1.011};
r_R_ranges_unscaled_1 = [0 7.7; 7.7 10.7; 10.7 14.7; 14.7 23.7;23.7 27.7;27.7 35.7;35.7 43.7;43.7 63]/R_1;
r_R_ranges_1 = r_R_ranges_unscaled_1 *sclaing_factor;

[theta_ideal_1, c_ideal_1] =  plot_design_curves(lambda_design, B, r_R, alpha_airfoils_1, cl_airfoils_1, r_R_ranges_1,R_1);

% - 2 = actual

data_blade = load("Blade_data.csv");
r_R_2 = data_blade(:,1)/R_1;
theta_ideal_2 = data_blade(:,3);
c_ideal_2 = data_blade(:,2);


%% Linear scaling KUBA
filename = "Scaled_blade.csv";
R = (118.5 - 3)/2; % Rotor radius (diameter minus 3 meters, then divided by 2)
R_orig = R_1;

R_range = r_R_2 * R; % Scale the radius

% Ensure all columns are column vectors
output_data = [R_range, c_ideal_2*R/R_1, theta_ideal_2*R/R_1];

% Convert to table with proper variable names
T = array2table(output_data, 'VariableNames', {'Radius_Meters', 'Twist_Degrees', 'Chord_Meters'});

% Save to CSV
writetable(T, filename);

disp('CSV file saved successfully.');


%% Plots

figure;
subplot(2, 1, 1);
plot(r_R, rad2deg(theta_ideal_1), 'LineWidth', 2);
hold on;
plot(r_R_2, theta_ideal_2, 'LineWidth', 2);
xlabel('r/R');
ylabel('\theta (degrees)');
title('Twist Distribution for All Airfoils');
xlim([0 1]);
ylim([0 15])
grid on;
legend('Analytical scaled', ' NFRE Scaled')

subplot(2, 1, 2);
plot(r_R, c_ideal_1, 'LineWidth', 2);
hold on;
plot(r_R_2, c_ideal_2, 'LineWidth', 2);
xlabel('r/R');
ylabel('c [m]');
title('Chord Distribution for All Airfoils');
grid on;
xlim([0 1]);

function [theta_ideal, c_ideal] = plot_design_curves(lambda_design, B, r_R, alpha_airfoils, cl_airfoils, r_R_ranges,R_1)

    if any(r_R_ranges(:) < 0) || any(r_R_ranges(:) > 1)
        error('r/R values must be between 0 and 1.');
    end
    
    theta_ideal = zeros(1, length(r_R)); 
    c_ideal = zeros(1, length(r_R)); 
    
    
    for i = 1:length(r_R)
        for j = 1:length(alpha_airfoils)
            if r_R(i) >= r_R_ranges(j, 1) && r_R(i) <= r_R_ranges(j, 2)
                alpha = deg2rad(alpha_airfoils{j});
                cl = cl_airfoils{j};
                
                theta_ideal(i) = (2/3) / (lambda_design * r_R(i)) - alpha;
                c_ideal(i) = (16/9) * (pi / (B * cl * lambda_design^2)) * (r_R(i) ^ -1) * R_1;
                
                break; 
            end
        end
    end
end
