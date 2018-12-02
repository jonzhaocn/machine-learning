function genetic_algorithm()
    % entry of genetic algorithm
    lower_bound = 0;
    upper_bound = 5;
    chromosome_length = 17;
    generation_count = 1000;
    population_size = 4;
    mutate_rate = 0.003;
    cross_rate = 0.8;
    population = init_population(population_size, chromosome_length);
    for iteration = 1:generation_count
        fitness = calculate_fitness(population, @fitness_function, lower_bound, upper_bound);
        plot_GA(population, fitness, @fitness_function, lower_bound, upper_bound);
        parent_selection_result = roulette_wheel_selection(fitness);
        offsprings = crossover(population, parent_selection_result, cross_rate);
        offsprings = mutation(offsprings, mutate_rate);
        offsprings_fitness = calculate_fitness(offsprings, @fitness_function, lower_bound, upper_bound);
        population = survivor_selection(population, offsprings, fitness, offsprings_fitness);
    end
end