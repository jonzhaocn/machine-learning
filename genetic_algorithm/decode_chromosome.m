function variables = decode_chromosome(chromosome, chromosome_length, bound)
    % decode chromosome to real number
    % input:
    %   chromosome:
    %   chromosome_length:
    %   bound:
    % output:
    %   variables: a cell
    variables = cell(1, numel(chromosome_length));
    for i=1:numel(chromosome_length)
        lower_bound = bound(2*i-1);
        upper_bound = bound(2*i);
        chromosome_size = chromosome_length(i);
        idx_start = sum(chromosome_length(1:i-1))+1;
        part_of_chro = chromosome(idx_start:idx_start+chromosome_length(i)-1, :);
        variable = pow2(size(part_of_chro,1)-1:-1:0) * part_of_chro;
        variable = lower_bound + variable * (upper_bound-lower_bound) / (2^chromosome_size-1);
        variables{i} = variable;
    end
end
