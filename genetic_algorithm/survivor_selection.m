function [population, fitness] = survivor_selection(population, offsprings, fitness, offsprings_fitness, min_or_max)
    % selecting survivor after generating offsprings
    if ~ismatrix(population)
        error('population should be a matrix')
    end
    if ~ismatrix(offsprings)
        error('offsprings should be a matrix')
    end
    if ~isvector(fitness)
        error('fitness should be a vector')
    end
    if ~isvector(offsprings_fitness)
        error('offsprings_fitness should be a vector')
    end
    if ~strcmp(min_or_max, 'min') && ~strcmp(min_or_max, 'max')
        error('min or max')
    end
    population_size = size(population, 1);
    % concat the poulation and offsprings and their fitness for sorting
    fitness = [fitness; offsprings_fitness];
    population = [population; offsprings];
    % selection based on the fitness value
    if strcmp(min_or_max, 'max')
        [fitness, index] = sort(fitness, 'descend');
    else
        [fitness, index] = sort(fitness);
    end
    population = population(index(1:population_size), :);
end