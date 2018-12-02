function offsprings = mutation(offsprings, mutate_rate)
    % mutation
    % input:
    %   population:
    %   mutate_rate:
    % output:
    %   offsprings:
    [chromosome_length, count] = size(offsprings);
    for i = 1:count
        if rand < mutate_rate
            mutate_position = round(rand * chromosome_length);
            if mutate_position == 0
                continue;
            end
            offsprings(mutate_position, i) = 1 - offsprings(mutate_position, i);
        end
    end
end