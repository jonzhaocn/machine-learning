function fitness = calculate_fitness(population, fitness_function, chromosome_length, bound)
    % calculate fitness of every individual according to fitness function
    % input:
    %   population:
    %   fitness_function:
    %   lower_bound:
    %   upper_bound:
    % output:
    %   fitness: vector of every individual's fitness
    
    input = decode_chromosome(population, chromosome_length, bound);
    fitness = fitness_function(input);
end