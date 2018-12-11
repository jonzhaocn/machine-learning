function offsprings = crossover(population, selection_result, chromosome_length, crossover_rate, crossover_operator)
    % crossover
    % input:
    %   population:
    %   selection_result:
    %   cross_rate:
    % output:
    %   offsprings:
    
    if ~ismatrix(population)
        error('population should be a matrix')
    end
    if ~isvector(selection_result)
        error('selection_result should be vector')
    end
    if ~isvector(chromosome_length)
        error('chromosome_length should be a vector')
    end
    if ~isscalar(crossover_rate)
        error('cross_rate should be a scalar')
    end
    if ~ischar(crossover_operator)
        error('crossover_operator should be a string')
    end
    
    offsprings = population(selection_result, :);
    
    % get start position of every variable in a chromosome
    idx_start = zeros(size(chromosome_length));
    for i=1:numel(idx_start)
        if i==1
            idx_start(i) = 1;
        else
            idx_start(i) = idx_start(i-1)+chromosome_length(i-1);
        end
    end
    % mutation
    if strcmp(crossover_operator, 'one_point_crossover')
        crossover_function = @one_point_crossover;
    elseif strcmp(crossover_operator, 'two_point_crossover')
        crossover_function = @two_point_crossover;
    elseif strcmp(crossover_operator, 'uniform_crossover')
        crossover_function = @uniform_crossover;
    else
        error('wrong crossover operator: %s', crossover_operator);
    end
    offsprings = crossover_function(offsprings, chromosome_length, idx_start, crossover_rate);
end

function offsprings = one_point_crossover(offsprings, chro_length, idx_start, crossover_rate)
    % for every pair of parents
    for i = 1:2:size(offsprings, 1)
        if rand < crossover_rate
            % for every variable in a chromosome
            for j =1:numel(chro_length)
                % get the crossover position
                cross_posi_start = idx_start(j)+round(chro_length(j)*rand())-1;
                if cross_posi_start == idx_start(j)-1 || cross_posi_start == idx_start(j)
                    continue
                end
                % crossover of two parnet and generate two offsprings
                cross_posi_end = idx_start(j)+chro_length(j)-1;
                temp = offsprings(i, :);
                offsprings(i, cross_posi_start:cross_posi_end) = offsprings(i+1, cross_posi_start:cross_posi_end);
                offsprings(i+1, cross_posi_start:cross_posi_end) = temp(cross_posi_start:cross_posi_end);
            end
        end
    end
end

function offsprings = two_point_crossover(offsprings, chro_length, idx_start, crossover_rate)
    % for every pair of parents
    for i = 1:2:size(offsprings, 1)
        if rand < crossover_rate
            % for every variable in a chromosome
            for j =1:numel(chro_length)
                % get the crossover position
                cross_posi_start = idx_start(j)+round(chro_length(j)*rand())-1;
                cross_posi_end = idx_start(j)+round(chro_length(j)*rand())-1;
                if cross_posi_end < cross_posi_start
                    temp = cross_posi_start;
                    cross_posi_start = cross_posi_end;
                    cross_posi_end = temp;
                end
                if cross_posi_start == idx_start(j)-1 || cross_posi_end == idx_start(j)-1 || ...
                        cross_posi_start == idx_start(j)+chro_length(j) || cross_posi_end == idx_start(j)+chro_length(j)
                    continue
                end
                % crossover of two parnet and generate two offsprings
                temp = offsprings(i, :);
                offsprings(i, cross_posi_start:cross_posi_end) = offsprings(i+1, cross_posi_start:cross_posi_end);
                offsprings(i+1, cross_posi_start:cross_posi_end) = temp(cross_posi_start:cross_posi_end);
            end
        end
    end
end

function offsprings = uniform_crossover(offsprings, chro_length, idx_start, crossover_rate)
    % for every pair of parents
    for i = 1:2:size(offsprings, 1)
        if rand < crossover_rate
             % for every variable in a chromosome
            for j =1:numel(chro_length)
                % get the crossover position
                cross_position = round(rand(chro_length(j),1));
                cross_position = find(cross_position==1)+idx_start(j)-1;
                % crossover of two parnet and generate two offsprings
                temp = offsprings(i, :);
                offsprings(i, cross_position) = offsprings(i+1, cross_position);
                offsprings(i+1, cross_position) = temp(cross_position);
            end
        end
    end
end