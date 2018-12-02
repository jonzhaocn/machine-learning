function population = init_population(population_size, chromosome_length)
    % initialize population
    % each column is a individual
    % input:
    %   population_size:
    %   chromosome_length:
    % output:
    %   population:
    population = round(rand(chromosome_length, population_size));
end