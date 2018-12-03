clc;
clear;
% testing example of function of two variables
% every chromosome represent two variables
% the first 25 numbers in chromosome represent x, the last 25 represent y
Setting.chromosome_length = [25, 25];
Setting.bound = [-10, 10, -10, 10];
Setting.generation_count = 100;
Setting.population_size = 10;
Setting.mutate_rate = 0.03;
Setting.cross_rate = 0.8;
Setting.fitness_function = @fitness_function2;
genetic_algorithm(Setting);

function result = fitness_function2(variables)
    x = variables{1};
    y = variables{2};
    result = x.^2+y.^2;
    result = 0.5 - ((sin(result.^0.5)).^2-0.5)./(1+0.001*result).^2;
end