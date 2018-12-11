function variables = decode_chromosome(chromosome, chromosome_length, LB, UB)
    % decode chromosome to real number
    % input:
    %   chromosome:
    %   chromosome_length: chromosome length of every variable
    %   bound: the lower bound and upper bound of every variable
    % output:
    %   variables: a cell
    if ~ismatrix(chromosome)
        error('chromosome should be a matrix')
    end
    if ~isvector(chromosome_length)
        error('chromosome_length should be a vector')
    end
    if ~isvector(LB) || ~isvector(UB)
        error('LB and UB should be a vector')
    end
    variables = cell(1, numel(chromosome_length));
    % for every variable in a chromosome
    for i=1:numel(chromosome_length)
        lower_bound = LB(i);
        upper_bound = UB(i);
        chromosome_size = chromosome_length(i);
        % get the according part of variable in chromosome
        idx_start = sum(chromosome_length(1:i-1))+1;
        part_of_chro = chromosome(:, idx_start:idx_start+chromosome_length(i)-1);
        % transform the chromosome to real number
        variable = part_of_chro * pow2(size(part_of_chro, 2)-1:-1:0)';
        variable = lower_bound + variable * (upper_bound-lower_bound) / (2^chromosome_size-1);
        variables{i} = variable;
    end
end
