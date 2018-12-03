function genetic_algorithm(Setting)
    % entry of genetic algorithm
    
    % ---- init setting
    bound = Setting.bound;
    chromosome_length = Setting.chromosome_length;
    generation_count = Setting.generation_count;
    population_size = Setting.population_size;
    mutate_rate = Setting.mutate_rate;
    cross_rate = Setting.cross_rate;
    fitness_function = Setting.fitness_function;
    % init population
    population = init_population(population_size, chromosome_length);
    % evolution
    for iteration = 1:generation_count
        fitness = calculate_fitness(population, fitness_function, chromosome_length, bound);
        plot_GA(population, fitness, fitness_function, chromosome_length, bound);
        parent_selection_result = roulette_wheel_selection(fitness);
        offsprings = crossover(population, parent_selection_result, chromosome_length, cross_rate);
        offsprings = mutation(offsprings, chromosome_length, mutate_rate);
        offsprings_fitness = calculate_fitness(offsprings, fitness_function, chromosome_length, bound);
        population = survivor_selection(population, offsprings, fitness, offsprings_fitness);
    end
end