function plot_GA(population, fitness, chromosome_length, bound, plot_variables, plot_R)
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
        error('chromosome_length shoule be a row vector of 1 or 2 length');
    end
    
    [~, max_index] = max(fitness);
    max_chromosome = population(:,max_index);
    max_var = decode_chromosome(max_chromosome, chromosome_length, bound);
    min_map = 0;
    for i = 1:numel(max_var)
        min_map = min_map + (plot_variables{i}-max_var{i}).^2;
    end
    min_map = min_map.^0.5;
    [~, index] = min(min_map(:));
    % delete last marked point
    obj = findobj('type', 'line', 'tag', 'max_fitness_point');
    delete(obj);
    % draw a new point
    if numel(chromosome_length)==1
        plot(plot_variables{1}(index), plot_R(index), 'ro', 'tag', 'max_fitness_point', 'MarkerEdgeColor', 'r', 'MarkerFaceColor', 'r');
    else
        plot3(plot_variables{1}(index), plot_variables{2}(index), plot_R(index), 'ro', 'tag', 'max_fitness_point', 'MarkerEdgeColor', 'r', 'MarkerFaceColor', 'r');
    end
    drawnow
%     pause(0.1);
end