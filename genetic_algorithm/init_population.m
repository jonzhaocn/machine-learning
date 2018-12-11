function population = init_population(population_size, chromosome_length)
    % initialize population
    % each row is a individual
    % input:
    %   population_size:
    %   chromosome_length:
    % output:
    %   population:
    if ~isscalar(population_size)
        error('population_size should be a scalar')
    end
    if ~isvector(chromosome_length)
        error('chromosome_length should be a vector')
    end
    chromosome_length = sum(chromosome_length);
    population = round(rand(population_size, chromosome_length));
end