function offsprings = crossover(population, selection_result, cross_rate)
    % crossover
    % input:
    %   population:
    %   selection_result:
    %   cross_rate:
    % output:
    %   offsprings:
    offsprings = population(:, selection_result);
    chromosome_size = size(population,1);
    for i = 1:2:numel(selection_result)
        if rand < cross_rate
            cross_position = round(chromosome_size*rand());
            if cross_position == 0 || cross_position == 1
                continue
            end
            % swap
            temp = offsprings(:,i);
            offsprings(cross_position:end, i) = offsprings(cross_position:end, i+1);
            offsprings(cross_position:end, i+1) = temp(cross_position:end);
        end
    end
end