function plot_GA(population, fitness, fitness_function, chromosome_length, bound)
    % plot the fitness function curve and mark the point which has the
    % biggest fitness
    % input:
    %   population:
    %   fitness:
    %   fitness_function:
    %   bound:
    % output:
    %   none
    if numel(chromosome_length)~=1 && numel(chromosome_length)~=2
        error('error');
    end
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
    R = fitness_function(variables);
    [~, max_index] = max(fitness);
    max_chromosome = population(:,max_index);
    max_var = decode_chromosome(max_chromosome, chromosome_length, bound);
    min_map = 0;
    for i = 1:numel(max_var)
        min_map = min_map + (variables{i}-max_var{i}).^2;
    end
    min_map = min_map.^0.5;
    [~, index] = min(min_map(:));
    if numel(chromosome_length)==1
        plot(variables{1}, R, '-o', 'MarkerIndices', index, 'MarkerEdgeColor', 'red', 'MarkerFaceColor', 'red');
        title('plot GA')
        xlabel('x')
        ylabel('fitness')
    else
        mesh(variables{1}, variables{2}, R);
    end
    drawnow
%     pause(0.1);
end