function plot_GA(population, fitness, chromosome_length, LB, UB, plot_variables, plot_R, min_or_max)
    % mark the point which has the largest fitness in population
    % biggest fitness
    % input:
    %   population:
    %   fitness:
    %   fitness_function:
    %   bound:
    % output:
    %   none
    
    if ~ismatrix(population)
        error('population should be a matrix')
    end
    if ~isvector(fitness)
        error('fitness should be a fitness')
    end
    if ~isvector(LB) || ~isvector(UB)
        error('LB and UB should be a vector')
    end
    if ~iscell(plot_variables)
        error('plot_variables should be a cell')
    end
    if ~ismatrix(plot_R)
        error('plot_R should be a matrix')
    end
    if numel(chromosome_length)~=1 && numel(chromosome_length)~=2
        error('chromosome_length shoule be a row vector of 1 or 2 length, only can plot curve or surface');
    end
    if ~strcmp(min_or_max, 'min') && ~strcmp(min_or_max, 'max')
        error('min or max')
    end
    if strcmp(min_or_max, 'max')
        [~, target_index] = max(fitness);
    else
        [~, target_index] = min(fitness);
    end
    % get the nearset point of target_var in plot_variables
    % and mark the nearest point in plot
    target_chromosome = population(target_index, :);
    target_var = decode_chromosome(target_chromosome, chromosome_length, LB, UB);
    min_map = 0;
    for i = 1:numel(target_var)
        min_map = min_map + (plot_variables{i}-target_var{i}).^2;
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