function x = decode(chromosome, lower_bound, upper_bound)
    % decode chromosome to real number
    % input:
    %   chromosome:
    %   lower_bound:
    %   upper_bound:
    % output:
    %   x: vector of numbers
    chromosome_size = size(chromosome, 1);
    x = pow2(size(chromosome,1)-1:-1:0) * chromosome;
    x = lower_bound + x * (upper_bound-lower_bound) / (2^chromosome_size-1);
end