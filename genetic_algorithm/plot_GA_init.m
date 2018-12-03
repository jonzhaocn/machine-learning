function [variables, R] = plot_GA_init(fitness_function, chromosome_length, bound)
    % plot the fitness funtion
    
    % check inputs
    if numel(chromosome_length)~=1 && numel(chromosome_length)~=2
        error('error');
    end
    % create variables as fitness function input 
    variables = cell(1, numel(chromosome_length));
    for i = 1:numel(chromosome_length)
        lower_bound = bound(2*i-1);
        upper_bound = bound(2*i);
        Fs = 100;            % Sampling frequency
        L = (upper_bound - lower_bound)*Fs;
        variables{i} = lower_bound + (0:L-1)/Fs;
    end
    if numel(chromosome_length)==2
        [variables{1}, variables{2}] = meshgrid(variables{1}, variables{2});
    end
    %----- plot fitness function
    R = fitness_function(variables);
    hold off
    if numel(chromosome_length)==1
        % plot curve
        plot(variables{1}, R);
        title('plot GA')
        xlabel('x')
        ylabel('fitness')
    else
        % plot surface
        mesh(variables{1}, variables{2}, R);
    end
    hold on 
    drawnow
end