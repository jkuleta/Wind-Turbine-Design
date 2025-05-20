clc; clear all; close all;

plot_response("Step_response_fixed_damp.mat", "Step_response_scheduled_damp.mat", "Fixed Gain", "Gain Scheduling", "Task 6 - Step_fixed_scheduled", false);
plot_response("Step_response_scheduled_damp.mat", "Step_response_scheduled_damp.mat", "No Damping", "With Damping", "Task 6 - Step_damp_nodamp", false);
plot_response("NMT_response_fixed_damp.mat", "NMT_response_scheduled_damp.mat", "Fixed Gain", "Gain Scheduling", "Task 6 - NMT_fixed_scheduled", true);
plot_response("NMT_response_scheduled_nodamp.mat", "NMT_response_scheduled_damp.mat", "No Damping", "With Damping", "Task 6 - NMT_damp_nodamp", true);

function plot_response(file1, file2, name1, name2, figname, remove)
    name1 = string(name1);
    name2 = string(name2);

    data1 = load(file1);
    data2 = load(file2);

    % Create a large figure
    fig = figure('Units', 'pixels', 'Position', [100, 100, 1400, 1000]);  % wider and taller

    if remove
        xlim_start = 60;
    else
        xlim_start = 0;
    end

    % Define common settings
    fontSize = 12;
    legendFontSize = 10;
    timeEnd = max(data1.Time);

    subplot(4,2,1);
    plot(data1.Time, data1.Wind1VelX, 'LineWidth', 1.5); hold on;
    plot(data2.Time, data2.Wind1VelX, 'LineWidth', 1.5);
    grid on;
    title('Wind Velocity [m/s]', 'FontSize', fontSize);
    lgd = legend(name1, name2, 'Location', 'best');
    set(lgd, 'FontSize', legendFontSize);
    xlim([xlim_start, timeEnd]);

    subplot(4,2,2);
    plot(data1.Time, data1.GenSpeed, 'LineWidth', 1.5); hold on;
    plot(data2.Time, data2.GenSpeed, 'LineWidth', 1.5);
    grid on;
    title('Generator Speed [rpm]', 'FontSize', fontSize);
    lgd = legend(name1, name2, 'Location', 'best');
    set(lgd, 'FontSize', legendFontSize);
    xlim([xlim_start, timeEnd]);

    subplot(4,2,3);
    plot(data1.Time, data1.GenPwr/1000, 'LineWidth', 1.5); hold on;
    plot(data2.Time, data2.GenPwr/1000, 'LineWidth', 1.5);
    grid on;
    title('Generator Power [kW]', 'FontSize', fontSize);
    lgd = legend(name1, name2, 'Location', 'best');
    set(lgd, 'FontSize', legendFontSize);
    xlim([xlim_start, timeEnd]);

    subplot(4,2,4);
    plot(data1.Time, data1.BlPitch1, 'LineWidth', 1.5); hold on;
    plot(data2.Time, data2.BlPitch1, 'LineWidth', 1.5);
    grid on;
    title('Blade Pitch Angle [deg]', 'FontSize', fontSize);
    lgd = legend(name1, name2, 'Location', 'best');
    set(lgd, 'FontSize', legendFontSize);
    xlim([xlim_start, timeEnd]);

    subplot(4,2,5);
    plot(data1.Time, data1.GenTq, 'LineWidth', 1.5); hold on;
    plot(data2.Time, data2.GenTq, 'LineWidth', 1.5);
    grid on;
    title('Generator Torque [Nm]', 'FontSize', fontSize);
    xlabel('Time [s]', 'FontSize', fontSize);
    lgd = legend(name1, name2, 'Location', 'best');
    set(lgd, 'FontSize', legendFontSize);
    xlim([xlim_start, timeEnd]);

    subplot(4,2,6);
    plot(data1.Time, data1.NcIMUTAxs, 'LineWidth', 1.5); hold on;
    plot(data2.Time, data2.NcIMUTAxs, 'LineWidth', 1.5);
    grid on;
    title('Nacelle Accel. Fore-aft [m/s^2]', 'FontSize', fontSize);
    xlabel('Time [s]', 'FontSize', fontSize);
    lgd = legend(name1, name2, 'Location', 'best');
    set(lgd, 'FontSize', legendFontSize);
    xlim([xlim_start, timeEnd]);

    subplot(4,2,7);
    plot(data1.Time, data1.NcIMUTAys, 'LineWidth', 1.5); hold on;
    plot(data2.Time, data2.NcIMUTAys, 'LineWidth', 1.5);
    grid on;
    title('Nacelle Accel. Side-to-side [m/s^2]', 'FontSize', fontSize);
    xlabel('Time [s]', 'FontSize', fontSize);
    lgd = legend(name1, name2, 'Location', 'best');
    set(lgd, 'FontSize', legendFontSize);
    xlim([xlim_start, timeEnd]);

    % Set paper size for proper export
    set(fig, 'PaperUnits', 'inches');
    set(fig, 'PaperPosition', [0 0 14 10]);  % [left, bottom, width, height]
    set(fig, 'PaperSize', [14 10]);

    % Save the figure
    saveas(fig, figname + ".png");
    % Optional: Save as .fig too
    % savefig(fig, figname + ".fig");
end