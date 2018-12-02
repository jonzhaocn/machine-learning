function [population, fitness] = survivor_selection(population, offsprings, fitness, offsprings_fitness)
    fitness = [fitness, offsprings_fitness];
    population = [population, offsprings];
    [fitness, index] = sort(fitness, 'descend');
    population = population(:, index);
end