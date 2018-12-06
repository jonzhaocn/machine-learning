% bit string version
%---------- script
clc;
clear;
global LB;
global UB;
global chromosome_length;
LB = [-5 -5];
UB = [5 5];
chromosome_length = [20 20];
nvars = sum(chromosome_length);
ObjectiveFunction = @fitness_function3;
% PopulationSize: 50 for five or fewer variables, otherwise 200
options = optimoptions(@ga,'PopulationSize',50, 'MaxGenerations',1000, ...
    'InitialPopulationMatrix', [], 'CrossoverFcn', @crossoversinglepoint, ...
    'MutationFcn', @mutationadaptfeasible, 'FunctionTolerance', 1e-6, 'PopulationType','bitstring',...
    'PlotFcn',{@gaplotbestf,@gaplotdistance,@gaplotrange}, 'Display','iter');
[x,fval,exitflag,output,population,scores] = ga(ObjectiveFunction,nvars,[],[],[],[],[],[], [], options);
x = decode_chromosome(x);
fprintf('best point is: [%s], and its fitness is %f\n', num2str(x), fval);
%-------------- function
% 
function y = fitness_function3(x)
    % option: rastriginsfcn min value is 0 at [0, 0]
    x = decode_chromosome(x);
    y = 10.0 * size(x,2) + sum(x .^2 - 10.0 * cos(2 * pi .* x),2);
end
function plot_fitness_function(func, LB, UB)
    % create variables as fitness function input
    if numel(LB)~=2 || numel(UB)~=2
        error('error')
    end
    variables = cell(1, numel(LB));
    for i = 1:numel(LB)
        lower_bound = LB(i);
        upper_bound = UB(i);
        Fs = 100;            % Sampling frequency
        L = (upper_bound - lower_bound)*Fs;
        variables{i} = lower_bound + (0:L-1)/Fs;
    end
    [X, Y] = meshgrid(variables{1}, variables{2});
    result = zeros(size(X));
    for i = 1:size(result, 1)
        for j = 1:size(result,2)
            result(i, j) = func([X(i, j), Y(i,j)]);
        end
    end
    figure(1);
    mesh(X, Y, result);
end
function result = decode_chromosome(chromosome)
    global LB;
    global UB;
    global chromosome_length;
    result = zeros(size(chromosome_length));
    for i=1:numel(chromosome_length)
        lower_bound = LB(i);
        upper_bound = UB(i);
        chromosome_size = chromosome_length(i);
        % get the according part of variable in chromosome
        idx_start = sum(chromosome_length(1:i-1))+1;
        part_of_chro = chromosome(idx_start:idx_start+chromosome_length(i)-1)';
        % transform the chromosome to real number
        variable = pow2(size(part_of_chro,1)-1:-1:0) * part_of_chro;
        variable = lower_bound + variable * (upper_bound-lower_bound) / (2^chromosome_size-1);
        result(i) = variable;
    end
end
