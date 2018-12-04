clc;
clear;
% testing example of function of two variables
% every chromosome represent two variables
% the first 25 numbers in chromosome represent x, the last 25 represent y
Setting.chromosome_length = [25, 25];
Setting.bound = [-10, 10, -10, 10];
Setting.generation_count = 1000;
Setting.population_size = 25;
Setting.mutation_rate = 0.03;
Setting.crossover_rate = 0.8;
Setting.fitness_function = @fitness_function2;
Setting.crossover_operator = 'one_point_crossover';
Setting.mutation_operator = 'bit_flip_mutation';
genetic_algorithm(Setting);

function result = fitness_function2(variables)
    x = variables{1};
    y = variables{2};
    result =sin(sqrt(x.^2+y.^2))./sqrt(x.^2+y.^2);
end