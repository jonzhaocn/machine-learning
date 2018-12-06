function plot_fitness_change(fitness)
    x = 1:numel(fitness);
    figure
    plot(x, fitness);
    title('fitness change')
    xlabel('generation')
    ylabel('best fitness')
end