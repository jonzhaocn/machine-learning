clc;
clear;
% testing example of function of one variable
% every chromosome represent a variable
Setting.chromosome_length = 17;
Setting.LB = 0;
Setting.UB = 5;
Setting.do_plot = true;
Setting.min_or_max = 'max';
Setting.generation_count = 100;
Setting.population_size = 10;
Setting.mutation_rate = 0.03;
Setting.crossover_rate = 0.8;
Setting.fitness_function = @fitness_function1;
Setting.crossover_operator = 'one_point_crossover';
Setting.mutation_operator = 'bit_flip_mutation';
target_fitness_change = genetic_algorithm(Setting);
plot_fitness_change(target_fitness_change)

function result = fitness_function1(variables)
    x = variables{1};
    result = sin(10*x).*x+cos(2*x).*x;
end
