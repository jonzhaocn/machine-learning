function [population, fitness] = survivor_selection(population, offsprings, fitness, offsprings_fitness)
    population_size = size(population, 2);
    fitness = [fitness, offsprings_fitness];
    population = [population, offsprings];
    [fitness, index] = sort(fitness, 'descend');
    population = population(:, index(1:population_size));
end