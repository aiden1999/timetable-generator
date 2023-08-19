"""Phase 4 (crossover) of genetic algorithm.

Functions:
    crossover(parent_a: list, parent_b: list, num_of_sessions: int,
        population_size: int) -> list
"""
import random
import math


def crossover(parents: list, population: list, population_size: int) -> list:
    """Crossover parents to produce offspring.

    Args:
        parents (list): # TODO fill this in
        population (list): # TODO fill this in
        population_size (int): The size of the population.

    Returns:
        list: The offspring.
    """
    offspring = []
    half_pop = math.ceil(population_size / 2)
    num_of_sessions = 
    for i in range(half_pop):
        
        # Select two parents to produce two offspring together
        parent_a = random.choice(parents)
        parents.remove(parent_a)
        parent_b = random.choice(parents)
        parents.remove(parent_b)
        
        
        
        # locus_outer: session that contains the split
        locus_outer = random.randint(0, num_of_sessions - 1)

        # locus_inner: split after session[locus_inner]
        if locus_outer == 0:
            locus_inner = random.randint(1, 2)  # TODO: hard coding fix?
        else:
            locus_inner = random.randint(0, 2)  # TODO: hard coding fix?

        # Crossover of child a
        left_a = parent_a[:locus_outer]
        centre_a = parent_a[locus_outer][:locus_inner] + \
            parent_b[locus_outer][locus_inner:]
        right_a = parent_b[locus_outer + 1:]
        left_a.append(centre_a)
        child_a = left_a + right_a
        offspring.append(child_a)

        # Crossover of child b
        left_b = parent_b[:locus_outer]
        centre_b = parent_b[locus_outer][:locus_inner] + \
            parent_a[locus_outer][locus_inner:]
        right_b = parent_a[locus_outer + 1:]
        left_b.append(centre_b)
        child_b = left_b + right_b
        offspring.append(child_b)

    # Remove last child if the population size is an odd number
    if half_pop != math.floor(population_size / 2):
        del offspring[-1]

    return offspring
