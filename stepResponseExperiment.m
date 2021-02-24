%stepResponseExperiment Script to plot data copied from serial monitor of
%arduino to estimate transfer function of motor
%
%
% This script requires data to be copied from serial monitor of arduino
% Type into Command Prompt:
%       Results = [];
%       openvar('Results');
%   Copy data from Aruduino Serial Monitor into spreadsheet that pops up
%
%% Define parameters and inputs

% Sampling time in seconds
t = (Results(:,1));

% Voltage command at sampling time
voltageCommand = Results(:,2);

% Velocity of wheel at sampling times
velocity = Results(:,3);

%% Plot results

figure(1)
plot(t,velocity)
title('Step response of experimental system')
xlabel('Time (s)')
ylabel('Velocity (m/s)')

% using the plot, determine transfer function of form: 
% K(sigma/(s+sigma))
% K = steady state value (5)
% sigma = 1/t (.934)
% t = time where velocity equals 0.64K (1.07)

%% Verify Velocity Transfer function

K = 5.25; %INSERT K VALUE CALCULATED ABOVE HERE
sigma = 14.28; %INSERT SIGMA VALUE HERE
num = K*sigma;
transferFunction = tf(num,[1 sigma]);

%plot step response
figure(2)
plot(T,stepped)
hold on
plot(t-1,velocity)
hold off
title('Comparing system responses')
xlabel('Time (ms)')
ylabel('Velocity (m/s)')

