function target_fitness_change = genetic_algorithm(Setting)
    % entry of genetic algorithm
    
    % ---- init setting
    LB = Setting.LB;
    UB = Setting.UB;
    chromosome_length = Setting.chromosome_length;
    generation_count = Setting.generation_count;
    population_size = Setting.population_size;
    mutation_rate = Setting.mutation_rate;
    crossover_rate = Setting.crossover_rate;
    fitness_function = Setting.fitness_function;
    crossover_operator = Setting.crossover_operator;
    mutation_operator = Setting.mutation_operator;
    min_or_max = Setting.min_or_max;
    do_plot = Setting.do_plot;
    % ---check
    if ~islogical(do_plot)
        error('do_plot should be logical')
    end
    % record
    target_fitness_change = zeros(1, generation_count);
    % init population
    population = init_population(population_size, chromosome_length);
    % init plot_GA, draw the fitness function
    if do_plot
        [plot_variables, plot_R] = plot_GA_init(fitness_function, chromosome_length, LB, UB);
    end
    % evolution
    for iteration = 1:generation_count
        fitness = calculate_fitness(population, fitness_function, chromosome_length, LB, UB);
        if strcmp(min_or_max, 'max')
            target_fitness_change(iteration) = max(fitness);
        else
            target_fitness_change(iteration) = min(fitness);
        end
        % mark the point which has the largest fitness in population
        if do_plot
            plot_GA(population, fitness, chromosome_length, LB, UB, plot_variables, plot_R, min_or_max);
        end
        % selection - crossover - mutation
        parent_selection_result = roulette_wheel_selection(fitness, min_or_max);
        offsprings = crossover(population, parent_selection_result, chromosome_length, crossover_rate, crossover_operator);
        offsprings = mutation(offsprings, chromosome_length, mutation_rate, mutation_operator);
        % survivor selection
        offsprings_fitness = calculate_fitness(offsprings, fitness_function, chromosome_length, LB, UB);
        population = survivor_selection(population, offsprings, fitness, offsprings_fitness, min_or_max);
    end
    fitness = calculate_fitness(population, fitness_function, chromosome_length, LB, UB);
    if strcmp(min_or_max, 'max')
        [target_fitness, target_index] = max(fitness);
    else
        [target_fitness, target_index] = min(fitness);
    end
    % print the target fitness
    target_chromosome = population(target_index, :);
    target_var = decode_chromosome(target_chromosome, chromosome_length, LB, UB);
    target_var = cellfun(@(x) x, target_var);
    fprintf('target_fitness is %f at point [%s]\n', target_fitness, num2str(target_var));
end