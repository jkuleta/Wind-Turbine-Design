files = dir('Files/*.mat');  % Load .mat files from 'Files'

% === Time Series Plot ===
figure('Name', 'Time Domain Comparison', 'Position', [100, 100, 1000, 600]);
titles_time = {'Time Series of NcIMUTAxs', 'Time Series of BlPitch1'};

for i = 1:2
    subplot(2,1,i); hold on; grid on;
    set(gca, 'FontSize', 12);
end

for k = 1:length(files)
    data = load(fullfile('Files', files(k).name));
    t = data.Time(:);
    x = data.NcIMUTAxs(:);
    y = data.BlPitch1(:);

    % Remove first 60 seconds
    idx = t >= 60;
    t = t(idx);
    x = x(idx);
    y = y(idx);

    subplot(2,1,1); plot(t, x, 'LineWidth', 1.5, 'DisplayName', files(k).name);
    subplot(2,1,2); plot(t, y, 'LineWidth', 1.5, 'DisplayName', files(k).name);
end

for i = 1:2
    subplot(2,1,i);
    title(titles_time{i}, 'FontSize', 14);
    xlabel('Time (s)', 'FontSize', 12);
    ylabel('Amplitude', 'FontSize', 12);
    legend('show', 'FontSize', 10);
end

% === Frequency Domain (FFT) Plot ===
figure('Name', 'Frequency Domain Comparison', 'Position', [100, 100, 1000, 600]);
titles_fft = {'Tower Fore-Aft Acceleration', 'Blade Pitch Angle'};

for i = 1:2
    subplot(2,1,i); hold on; grid on;
    set(gca, 'YScale', 'log', 'FontSize', 12);
end

for k = 1:length(files)
    data = load(fullfile('Files', files(k).name));
    t = data.Time(:);
    x = data.NcIMUTAxs(:);
    y = data.BlPitch1(:);

    % Remove first 60 seconds
    idx = t >= 60;
    t = t(idx);
    x = x(idx);
    y = y(idx);

    % FFT setup using Welch
    dt = t(2) - t(1);
    [X, f_welch] = pwelch(x, [], [], [], 1/dt);
    [Y, ~] = pwelch(y, [], [], [], 1/dt);

    % Frequency axis limit
    idx_f = f_welch <= 10;
    f = f_welch(idx_f);
    X = X(idx_f);
    Y = Y(idx_f);

    subplot(2,1,1); plot(f, X, 'LineWidth', 1.5);
    subplot(2,1,2); plot(f, Y, 'LineWidth', 1.5);
end

legend_labels = {'Damping gain: K=0', 'Damping gain: K=0.1', 'Damping gain: K=0.15', 'Damping gain: K=0.18','Damping gain: K=0.2', 'Damping gain: K=0.3'};

for i = 1:2
    subplot(2,1,i);
    title(titles_fft{i}, 'FontSize', 14);
    xlabel('Frequency (Hz)', 'FontSize', 12);
    ylabel('Magnitude', 'FontSize', 12);
    legend(legend_labels, 'FontSize', 10);
    xlim([0 4]);
end
