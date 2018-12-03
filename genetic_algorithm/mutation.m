function offsprings = mutation(offsprings, chromosome_length, mutate_rate)
    % mutation
    % input:
    %   population:
    %   chromosome_length:
    %   mutate_rate:
    % output:
    %   offsprings:
    
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
    
    % mutation
    for i = 1:size(offsprings,2)
        if rand < mutate_rate
            for j=1:numel(chromosome_length)
                % get mutation positon
                mutation_position = idx_start(j) + round(rand * chromosome_length(j))-1;
                if mutation_position == idx_start(j)-1
                    continue;
                end
                offsprings(mutation_position, i) = 1 - offsprings(mutation_position, i);
            end
        end
    end
end