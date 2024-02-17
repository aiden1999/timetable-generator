"""Phase 4 (crossover) of genetic algorithm.

Functions:
    crossover(chosen_parents: list) -> [list, list]
"""
import copy
import random
import math


def crossover(parent_list: list) -> [list, list]:
    """Crossover parents to produce offspring.

    Args:
        chosen_parents (list): The parents used to create the offspring.

    Returns:
        list: The offspring.
        list: Unmodified copy of the parents.
    """
    offspring = []
    parent_list_copy = copy.deepcopy(parent_list)
    num_of_sessions = len(parent_list[0])

    for i in range(int(len(parent_list_copy) / 2)):

        # Select two parents to produce two offspring together
        parent_a = random.choice(parent_list)
        parent_list.remove(parent_a)
        parent_b = random.choice(parent_list)
        parent_list.remove(parent_b)

        for i in range(2):

            # locus_outer: session that contains :while condition:
            locus_outer = random.randint(0, num_of_sessions - 1)

            # locus_inner: split after session[locus_inner]
            if locus_outer == 0:
                locus_inner = random.randint(1, 2)
            else:
                locus_inner = random.randint(0, 2)

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

    return offspring, parent_list_copy
