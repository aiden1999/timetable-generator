"""Phase 3 (selection) of genetic algorithm.

Functions:
    select_parents(population_fitness: list) -> [int, int]
    normalise_values(fitness_values: list) -> list
    choose_parent(range_limits: list) -> int
"""
import random


def select_parents(population_fitness: list) -> [int, int]:
    """Select the parents for crossover.

    Args:
        population_fitness (list): The fitness values of the population.

    Returns:
        int: Index of the first parent.
        int: Index of the other parent.
    """
    # print("Selecting parents for crossover...") TODO: add back
    fitness_values = population_fitness
    range_limits_a = normalise_values(fitness_values)
    parent_a = choose_parent(range_limits_a)
    # print("First parent selected.") TODO: add back
    fitness_values.remove(fitness_values[parent_a])

    range_limits_b = normalise_values(fitness_values)
    parent_b = choose_parent(range_limits_b)
    # print("Second parent selected.") TODO: add back
    return parent_a, parent_b


def normalise_values(fitness_values: list) -> list:
    """Normalise the fitness values so that they add up to 1.

    Args:
        fitness_values (list): The fitness values of the population.

    Returns:
        list: Cumulative sums of the normalised fitness values.
    """
    fitness_total = 0
    for value in fitness_values:
        fitness_total += value
    range_limits = []
    for i in range(len(fitness_values)):
        value_norm = fitness_values[i] / fitness_total
        range_limits.append(value_norm)
        if i != 0:
            range_limits[i] += range_limits[i - 1]
    range_limits[len(fitness_values) - 1] = 1
    range_limits.insert(0, 0)
    return range_limits  # limits are upper limits?


def choose_parent(range_limits: list) -> int:
    """Perform a binary search to get the index of the chosen parent.

    Args:
        range_limits (list): Cumulative sums of the normalised fitness values.

    Returns:
        int: The index of the chosen parent.
    """
    choice = random.random()
    lower, upper = 0, len(range_limits) - 1
    found_parent = False
    parent_index = None
    while not found_parent:
        middle = (lower + upper) // 2
        if lower == upper - 1:
            found_parent = True
            parent_index = middle
        elif range_limits[middle] < choice:
            lower = middle
        else:
            upper = middle
    return parent_index
