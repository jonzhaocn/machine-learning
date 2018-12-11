clc;
clear;
% testing example of function of two variables
% every chromosome represent two variables
% the first 25 numbers in chromosome represent x, the last 25 represent y
Setting.chromosome_length = [15, 15, 15, 15];
Setting.LB = [-5, -5, -5, -5];
Setting.UB = [5, 5, 5, 5];
Setting.generation_count = 500;
Setting.population_size = 50;
Setting.mutation_rate = 0.01;
Setting.crossover_rate = 0.8;
Setting.fitness_function = @fitness_function5;
% crossover_operator: one_point_crossover, two_point_crossover, uniform_crossover
Setting.crossover_operator = 'two_point_crossover';
% mutation_operator: bit_flip_mutation, swap_mutation, scramble_mutation, inversion_mutation
Setting.mutation_operator = 'bit_flip_mutation';
Setting.min_or_max = 'min';
Setting.do_plot = false;
target_fitness_change = genetic_algorithm(Setting);
plot_fitness_change(target_fitness_change)

function result = fitness_function2(variables)
    % min value is -1 at [0, 0]
    if numel(variables)~=2
        error('numel(variables) should equal to 2')
    end
    x = variables{1};
    y = variables{2};
    result = x.^2 + y.^2;
    result = 0.5 - (sin(sqrt(result)).^2-0.5)./(1+0.001*result).^2;
end
function result = fitness_function3(variables)
    % min value is 0 at [1, 1]
    if numel(variables)~=2
        error('numel(variables) should equal to 2')
    end
    x = variables{1};
    y = variables{2};
    result = 100 * (x.^2 - y).^2 + (1 - x).^2;
end
function result = fitness_function4(variables)
    % rastriginsfcn min value is 0 at [0, 0]
    D = numel(variables);
    if D<=0
        error('numel(variables) should >= 1')
    end
    result = zeros(size(variables{1}));
    for i = 1:D
        result = result + variables{i}.^2 - 10.0*cos(2*pi*variables{i});
    end
    result = result + 10 * D;
end
function result = fitness_function5(variables)
    % sphere function min value is 0 at [0, 0]
    D = numel(variables);
    if D<=0
        error('numel(variables) should >= 1')
    end
    result = zeros(size(variables{1}));
    for i = 1:D
        result = result + variables{i}.^2;
    end
end
function result = fitness_function6(variables)
    % salomon function min is 0 at [0, 0]
    D = numel(variables);
    if D<=0
        error('numel(variables) should >= 1')
    end
    result = zeros(size(variables{1}));
    for i = 1:D
        result = result + variables{i}.^2;
    end
    result = sqrt(result);
    result = -1*cos(2*pi*result) + 0.1*result+1;
end
function result = fitness_function7(variables)
    % hyper-ellipsoid function min is 0 at [0, 0]
    D = numel(variables);
    if D<=0
        error('numel(variables) should >= 1')
    end
    result = zeros(size(variables{1}));
    for i = 1:D
        result = result + i * variables{i}.^2;
    end
end