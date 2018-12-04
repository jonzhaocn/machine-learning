function genetic_algorithm(Setting)
    % entry of genetic algorithm
    
    % ---- init setting
    bound = Setting.bound;
    chromosome_length = Setting.chromosome_length;
    generation_count = Setting.generation_count;
    population_size = Setting.population_size;
    mutation_rate = Setting.mutation_rate;
    crossover_rate = Setting.crossover_rate;
    fitness_function = Setting.fitness_function;
    crossover_operator = Setting.crossover_operator;
    mutation_operator = Setting.mutation_operator;
    % init population
    population = init_population(population_size, chromosome_length);
    % init plot_GA, draw the fitness function
    [plot_variables, plot_R] = plot_GA_init(fitness_function, chromosome_length, bound);
    % evolution
    for iteration = 1:generation_count
        fitness = calculate_fitness(population, fitness_function, chromosome_length, bound);
        % mark the point which has the largest fitness in population
        plot_GA(population, fitness, chromosome_length, bound, plot_variables, plot_R);
        % selection - crossover - mutation
        parent_selection_result = roulette_wheel_selection(fitness);
        offsprings = crossover(population, parent_selection_result, chromosome_length, crossover_rate, crossover_operator);
        offsprings = mutation(offsprings, chromosome_length, mutation_rate, mutation_operator);
        % survivor selection
        offsprings_fitness = calculate_fitness(offsprings, fitness_function, chromosome_length, bound);
        population = survivor_selection(population, offsprings, fitness, offsprings_fitness);
    end
end