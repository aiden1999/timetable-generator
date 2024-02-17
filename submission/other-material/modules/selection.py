"""Phase 3 (selection) of genetic algorithm.

Functions:
    select_parents(pop_fitness: list, population_size: int)
        -> [list, int]
"""
import math


def select_parents(pop_fitness: list, population_size: int) \
        -> [list, int]:
    """Select the parents for crossover.

    Args:
        pop_fitness (list): The fitness values of the population.
        population_size (int): The size of the population.

    Returns:
        list: The chosen parents
        int: Fitness of the chosen parent with the worst fitness
    """
    parents = []
    sorted_fitness = pop_fitness
    sorted_fitness.sort(key=lambda x: x[1])
    for i in range(2 * math.ceil(population_size / 4)):
        parent = sorted_fitness[0][0]
        parents.append(parent)
        if i == (2 * math.ceil(population_size/4)) - 1:
            worst_parent_fitness = sorted_fitness[0][1]
        del sorted_fitness[0]
    return parents, worst_parent_fitness
