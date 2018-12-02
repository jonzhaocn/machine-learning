function plot_GA(population, fitness, fitness_function, lower_bound, upper_bound)
    % plot the fitness function curve and mark the point which has the
    % biggest fitness
    Fs = 100;            % Sampling frequency                    
    L = (upper_bound - lower_bound)*Fs;
    X = lower_bound + (0:L)/Fs;
    Y = fitness_function(X);
    
    [~, max_index] = max(fitness);
    max_chromosome = population(:,max_index);
    max_x = decode(max_chromosome, lower_bound, upper_bound);
    [~, index] = min(abs(X-max_x));
    plot(X, Y, '-o', 'MarkerIndices', index, 'MarkerEdgeColor', 'red', 'MarkerFaceColor', 'red');
    title('plot GA')
    xlabel('x')
    ylabel('fitness')
    pause(0.1);
end