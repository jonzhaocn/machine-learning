function fitness = calculate_fitness(population, fitness_function, chromosome_length, bound)
    % calculate fitness of every individual according to fitness function
    % input:
    %   population:
    %   fitness_function:
    %   lower_bound:
    %   upper_bound:
    % output:
    %   fitness: vector of every individual's fitness
    if ~ismatrix(population)
        error('population should be a matrix')
    end
    if ~isa(fitness_function, 'function_handle')
        error('fitness_function should be a function handle')
    end
    if ~isvector(chromosome_length)
        error('chromosome_length should be a vector')
    end
    if ~isvector(bound)
        error('bound should be a vector')
    end
    input = decode_chromosome(population, chromosome_length, bound);
    fitness = fitness_function(input);
end