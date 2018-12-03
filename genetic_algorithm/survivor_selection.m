function [population, fitness] = survivor_selection(population, offsprings, fitness, offsprings_fitness)
    % selecting survivor after generating offsprings
    population_size = size(population, 2);
    fitness = [fitness, offsprings_fitness];
    population = [population, offsprings];
    % selection based on the fitness value
    [fitness, index] = sort(fitness, 'descend');
    population = population(:, index(1:population_size));
end