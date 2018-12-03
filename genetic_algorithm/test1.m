clc;
clear;
% testing example of function of one variable
% every chromosome represent a variable
Setting.chromosome_length = 17;
Setting.bound = [0, 5];
Setting.generation_count = 100;
Setting.population_size = 10;
Setting.mutate_rate = 0.03;
Setting.cross_rate = 0.8;
Setting.fitness_function = @fitness_function1;
genetic_algorithm(Setting);

function result = fitness_function1(variables)
    x = variables{1};
    result = sin(10*x).*x+cos(2*x).*x;
end
