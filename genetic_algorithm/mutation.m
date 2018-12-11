function offsprings = mutation(offsprings, chromosome_length, mutation_rate, mutation_operator)
    % mutation
    % input:
    %   population:
    %   chromosome_length:
    %   mutation_rate:
    % output:
    %   offsprings:
    
    if ~ismatrix(offsprings)
        error('offsprings should be a matrix')
    end
    if ~isvector(chromosome_length)
        error('chromosome_length should be a vector')
    end
    if ~isscalar(mutation_rate)
        error('mutation_rate should be a scalar')
    end
    if ~ischar(mutation_operator)
        error('mutation_operator should be a string')
    end
    
    % get position of every variable in chromosome
    idx_start = zeros(size(chromosome_length));
    for i=1:numel(idx_start)
        if i==1
            idx_start(i)=1;
        else
            idx_start(i) = idx_start(i-1)+chromosome_length(i-1);
        end
    end
    
    % mutation
    if strcmp(mutation_operator, 'bit_flip_mutation')
        mutation_function = @bit_flip_mutation;
    elseif strcmp(mutation_operator, 'swap_mutation')
        mutation_function = @swap_mutation;
    elseif strcmp(mutation_operator, 'scramble_mutation')
        mutation_function = @scramble_mutation;
    elseif strcmp(mutation_operator, 'inversion_mutation')
        mutation_function = @inversion_mutation;
    else
        error('wrong mutation operator: %s', mutation_operator);
    end
    offsprings = mutation_function(offsprings, chromosome_length, idx_start, mutation_rate);
end

function offsprings = bit_flip_mutation(offsprings, chromosome_length, idx_start, mutation_rate)
% reference: https://www.tutorialspoint.com/genetic_algorithms/genetic_algorithms_mutation.htm
% In this bit flip mutation, we select one or more random bits and flip 
% them. This is used for binary encoded GAs.
    for i = 1:size(offsprings, 1)
        if rand < mutation_rate
            for j=1:numel(chromosome_length)
                % get mutation positon
                mutation_position = idx_start(j) + round(rand * chromosome_length(j))-1;
                if mutation_position == idx_start(j)-1
                    continue;
                end
                offsprings(i, mutation_position) = 1 - offsprings(i, mutation_position);
            end
        end
    end
end
function offsprings = swap_mutation(offsprings, chromosome_length, idx_start, mutation_rate)
% In swap mutation, we select two positions on the chromosome at random, 
% and interchange the values.
    for i = 1:size(offsprings, 1)
        if rand < mutation_rate
            for j=1:numel(chromosome_length)
                % get mutation positon
                mutation_position = idx_start(j) + round(rand(1, 2) * chromosome_length(j))-1;
                if numel(find(mutation_position==idx_start(j)-1))~=0
                    continue;
                end
                temp = offsprings(i, mutation_position(1));
                offsprings(i, mutation_position(1)) = offsprings(i, mutation_position(2));
                offsprings(i, mutation_position(2)) = temp;
            end
        end
    end
end
function offsprings = scramble_mutation(offsprings, chromosome_length, idx_start, mutation_rate)
% In this, from the entire chromosome, a subset of genes is chosen 
% and their values are scrambled or shuffled randomly.
    for i = 1:size(offsprings, 1)
        if rand < mutation_rate
            for j=1:numel(chromosome_length)
                % get mutation positon
                muta_posi_start = idx_start(j)+round(chromosome_length(j)*rand())-1;
                muta_posi_end = idx_start(j)+round(chromosome_length(j)*rand())-1;
                if muta_posi_end < muta_posi_start
                    temp = muta_posi_start;
                    muta_posi_start = muta_posi_end;
                    muta_posi_end = temp;
                end
                if muta_posi_start==0 || muta_posi_end==0 || muta_posi_start==idx_start(j)+chromosome_length(j) ...
                        || muta_posi_end==idx_start(j)+chromosome_length(j)
                    continue;
                end
                temp = offsprings(i, muta_posi_start:muta_posi_end);
                temp = temp(randperm(numel(temp)));
                offsprings(i, muta_posi_start:muta_posi_end) = temp;
            end
        end
    end
end
function offsprings = inversion_mutation(offsprings, chromosome_length, idx_start, mutation_rate)
% In inversion mutation, we select a subset of genes like in scramble 
% mutation, but instead of shuffling the subset, we merely invert the 
% entire string in the subset.
    % get mutation positon
    for i = 1:size(offsprings, 1)
        if rand < mutation_rate
            for j=1:numel(chromosome_length)
                % get mutation positon
                muta_posi_start = idx_start(j)+round(chromosome_length(j)*rand())-1;
                muta_posi_end = idx_start(j)+round(chromosome_length(j)*rand())-1;
                if muta_posi_end < muta_posi_start
                    temp = muta_posi_start;
                    muta_posi_start = muta_posi_end;
                    muta_posi_end = temp;
                end
                if muta_posi_start==0 || muta_posi_end==0 || muta_posi_start==idx_start(j)+chromosome_length(j) ...
                        || muta_posi_end==idx_start(j)+chromosome_length(j)
                    continue;
                end
                offsprings(i, muta_posi_start:muta_posi_end) = offsprings(i, muta_posi_end:-1:muta_posi_start);
            end
        end
    end
end