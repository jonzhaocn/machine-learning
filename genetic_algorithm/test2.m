clc;
clear;
% testing example of function of two variables
% every chromosome represent two variables
% the first 25 numbers in chromosome represent x, the last 25 represent y
Setting.chromosome_length = [25, 25];
Setting.bound = [-10, 10, -10, 10];
Setting.generation_count = 200;
Setting.population_size = 50;
Setting.mutation_rate = 0.03;
Setting.crossover_rate = 0.8;
Setting.fitness_function = @fitness_function4;
% crossover_operator: one_point_crossover, multi_point_crossover, uniform_crossover
Setting.crossover_operator = 'one_point_crossover';
% mutation_operator: bit_flip_mutation, swap_mutation, scramble_mutation, inversion_mutation
Setting.mutation_operator = 'bit_flip_mutation';
Setting.min_or_max = 'min';
genetic_algorithm(Setting);

function result = fitness_function2(variables)
    % min value is -1 at [0, 0]
    x = variables{1};
    y = variables{2};
    result = x.^2 + y.^2;
    result = 0.5 - (sin(sqrt(result)).^2-0.5)./(1+0.001*result).^2;
end
function result = fitness_function3(variables)
    % min value is 0 at [1, 1]
    x = variables{1};
    y = variables{2};
    result = 100 * (x.^2 - y).^2 + (1 - x).^2;
end
function result = fitness_function4(variables)
    % rastriginsfcn min value is 0 at [0, 0]
    x = variables{1};
    y = variables{2};
    result = 20.0+(x.^2 - 10.0*cos(2*pi*x))+(y.^2 - 10.0*cos(2*pi*y));
end