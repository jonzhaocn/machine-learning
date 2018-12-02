function new_population = crossover(population, selection_result, cross_rate)
    % crossover
    % input:
    %   population:
    %   selection_result:
    %   cross_rate:
    % output:
    %   new_population:
    new_population = zeros(size(population,1), numel(selection_result));
    chromosome_size = size(population,1);
    for i = 1:2:numel(selection_result)
        new_population(:, [i,i+1]) = population(:, selection_result([i,i+1]));
        if rand < cross_rate
            cross_position = round(chromosome_size*rand());
            if cross_position == 0 || cross_position == 1
                continue
            end
            % swap
            temp = new_population(:,i);
            new_population(cross_position:end, i) = new_population(cross_position:end, i+1);
            new_population(cross_position:end, i+1) = temp(cross_position:end);
        end
    end
end