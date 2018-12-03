function offsprings = crossover(population, selection_result, chromosome_length, cross_rate)
    % crossover
    % input:
    %   population:
    %   selection_result:
    %   cross_rate:
    % output:
    %   offsprings:
    offsprings = population(:, selection_result);
    
    % get position of every variable in chromosome
    idx_start = zeros(size(chromosome_length));
    idx_end = zeros(size(chromosome_length));
    for i=1:numel(idx_start)
        if i==1
            idx_start(i)=1;
            idx_end(i)=chromosome_length(1);
        else
            idx_start(i) = idx_end(i-1)+1;
            idx_end(i) = idx_end(i-1)+chromosome_length(i);
        end
    end
    % for every parent
    for i = 1:2:numel(selection_result)
        if rand < cross_rate
            % for every part of chromosome
            for j =1:numel(chromosome_length)
                cross_position = idx_start(j)+round(chromosome_length(j)*rand())-1;
                if cross_position == idx_start(j)-1 || cross_position == idx_start(j)
                    continue
                end
                % crossover two offsprings
                temp = offsprings(:,i);
                offsprings(cross_position:idx_end(j), i) = offsprings(cross_position:idx_end(j), i+1);
                offsprings(cross_position:idx_end(j), i+1) = temp(cross_position:idx_end(j));
            end
        end
    end
end