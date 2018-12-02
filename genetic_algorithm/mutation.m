function population = mutation(population, mutate_rate)
    % mutation
    % input:
    %   population:
    %   mutate_rate:
    % output:
    %   population:
    [chromosome_length, population_size] = size(population);
    for i = 1:population_size
        if rand < mutate_rate
            mutate_position = round(rand * chromosome_length);
            if mutate_position == 0
                continue;
            end
            population(mutate_position, i) = 1 - population(mutate_position, i);
        end
    end
end