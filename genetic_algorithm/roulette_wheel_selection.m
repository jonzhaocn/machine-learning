function selection_result = roulette_wheel_selection(fitness, min_or_max)
    % roulette wheel selection
    % input:
    %   fitness: fitness vector of every individual
    % output:
    %   selection_result: array of index of selected individuals
    if ~isvector(fitness)
        error('fitness function should be a vector')
    end
    if ~strcmp(min_or_max, 'min') && ~strcmp(min_or_max, 'max')
        error('min or max')
    end
    population_size = size(fitness, 1);
    % normalize fitness values
    % ----
    if strcmp(min_or_max, 'max')
        min_fit = min(fitness);
        fitness = fitness - min_fit;
    else 
        fitness = -fitness;
        min_fit = min(fitness);
        fitness = fitness - min_fit;
    end
    % create roulette wheel
    sum_fit = sum(fitness);
    wheel = zeros(size(fitness));
    for i = 1:numel(fitness)
        if i==1
            wheel(i) = fitness(i);
        else
            wheel(i) = wheel(i-1) + fitness(i);
        end
    end
    wheel = wheel / sum_fit;
    % start selecting
    selection_result = zeros(1, floor((population_size+1)/2)*2);
    for i = 1:floor((population_size+1)/2)*2
        selection_result(i) = bi_search(wheel, rand());
%         selection_result(i+1) = mod(selection_result(i), population_size)+1;
    end
end

function idx = bi_search(wheel, value)
    % binary search
    % input:
    %   wheel: ordered array
    %   value: target value
    % output:
    %   idx: index of target value in wheel
    first = 1;
    last = size(wheel, 1);
    idx = -1;
    while first<last && idx==-1
        mid = round((first+last)/2);
        if value > wheel(mid)
            first = mid;
        elseif value < wheel(mid)
            last = mid;
        else
            idx = mid;
        end
        if last-first == 1
            idx = last;
            break;
        end
    end
end