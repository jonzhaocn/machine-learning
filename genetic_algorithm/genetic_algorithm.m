function genetic_algorithm()
    % entry of genetic algorithm
    lower_bound = 0;
    upper_bound = 5;
    chromosome_length = 17;
    generation_count = 1000;
    population_size = 25;
    mutate_rate = 0.003;
    cross_rate = 0.8;
    population = init_population(population_size, chromosome_length);
    for iteration = 1:generation_count
        fitness = calculate_fitness(population, @fitness_function, lower_bound, upper_bound);
        plot_GA(population, fitness, @fitness_function, lower_bound, upper_bound);
        selection_result = roulette_wheel_selection(fitness);
        population = crossover(population, selection_result, cross_rate);
        population = mutation(population, mutate_rate);
    end
end