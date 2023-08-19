"""Phase 3 (selection) of genetic algorithm.

Functions:
    select_parents(population_fitness: list, population_size: int) -> list
"""
import math


def select_parents(population_fitness: list, population_size: int) \
        -> list:
    """Select the parents for crossover.

    Args:
        population_fitness (list): The fitness values of the population.

    Returns:
        list: Indexes of the chosen parents
    """
    parents = []
    fitness_values = population_fitness
    for i in range(math.ceil(population_size / 2)):
        parent = fitness_values.index(min(fitness_values))
        parents.append(parent)
    return parents
