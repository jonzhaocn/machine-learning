function selection_result = roulette_wheel_selection(fitness)
    % roulette wheel selection
    % input:
    %   fitness: fitness vector of every individual
    % output:
    %   selection_result: array of index of selected individuals
    population_size = size(fitness,2);
    % normalize fitness values
    min_fit = min(fitness);
    fitness = fitness - min_fit;
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
    for i = 1:2:floor((population_size+1)/2)*2
        selection_result(i) = bi_search(wheel, rand());
        selection_result(i+1) = mod(selection_result(i), population_size)+1;
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
    last = size(wheel, 2);
    idx = -1;
    while first<last && idx==-1
        mid = round((first+last)/2);
        if value > wheel(mid)
            first = mid+1;
        elseif value < wheel(mid)
            last = mid-1;
        else
            idx = mid;
        end
        if last-first <=1
            idx = last;
            break;
        end
    end
end