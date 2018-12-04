function [population, fitness] = survivor_selection(population, offsprings, fitness, offsprings_fitness)
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
    population_size = size(population, 2);
    fitness = [fitness, offsprings_fitness];
    population = [population, offsprings];
    % selection based on the fitness value
    [fitness, index] = sort(fitness, 'descend');
    population = population(:, index(1:population_size));
end