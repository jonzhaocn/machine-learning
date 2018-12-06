% reference:
%   https://ww2.mathworks.cn/help/gads/ga.html
%   https://ww2.mathworks.cn/help/gads/genetic-algorithm.html
%   https://ww2.mathworks.cn/help/gads/vary-mutation-and-crossover.html
%   https://ww2.mathworks.cn/help/gads/genetic-algorithm-options.html
%---------- script
clc;
clear;
ObjectiveFunction = @fitness_function1;
nvars = 2;
LB = [-5 -5];
UB = [5 5];
plot_fitness_function(ObjectiveFunction, LB, UB);
% PopulationSize: 50 for five or fewer variables, otherwise 200
options = optimoptions(@ga,'PopulationSize',50, 'MaxGenerations',1000, ...
    'InitialPopulationMatrix', [], 'CrossoverFcn', @crossoverintermediate, ...
    'MutationFcn', @mutationadaptfeasible, 'FunctionTolerance', 1e-6, 'PopulationType','doublevector',...
    'PlotFcn',{@gaplotbestf,@gaplotdistance,@gaplotrange}, 'Display','iter');
[x,fval] = ga(ObjectiveFunction,nvars,[],[],[],[],LB,UB, [], options);
fprintf('best point is: [%s], and its fitness is %f\n', num2str(x), fval);
%-------------- function
% option: rastriginsfcn min value is 0 at [0, 0]
% 
function y = fitness_function1(x)
    % https://ww2.mathworks.cn/help/gads/fitness-function-forms.html
    % min value is 0 at [1, 1]
    y = 100 * (x(1)^2 - x(2)) ^2 + (1 - x(1))^2;
end
function y = fitness_function2(x)
    % http://garfileo.is-programmer.com/2011/2/19/hello-ga.24563.html
    % min value is -1 at [0, 0]
    y = x(1)*x(1)+x(2)*x(2);
    y = -0.5 + (sin(sqrt(y))^2-0.5)/(1+0.001*y)^2; 
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