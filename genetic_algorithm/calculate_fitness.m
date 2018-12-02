function fitness = calculate_fitness(population, fitness_function, lower_bound, upper_bound)
    % calculate fitness of every individual
    % input:
    %   population:
    %   fitness_function:
    %   lower_bound:
    %   upper_bound:
    % output:
    %   fitness: vector of every individual's fitness
    input = decode(population, lower_bound, upper_bound);
    fitness = fitness_function(input);
end