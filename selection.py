import random


def select_parents(population_fitness):
    """_summary_

    Args:
        population_fitness (_type_): _description_

    Returns:
        _type_: _description_
    """
    print("Selecting parents for crossover...")
    fitness_values = population_fitness
    print(len(fitness_values))
    range_limits_a = normalise_values(fitness_values)
    print(range_limits_a)  # debugging TODO: remove later
    parent_a = choose_parent(range_limits_a)
    print("First parent selected.")
    fitness_values.remove(fitness_values[parent_a])
    print(len(fitness_values))
    range_limits_b = normalise_values(fitness_values)
    parent_b = choose_parent(range_limits_b)
    print(str(parent_b))  # debugging TODO: remove later
    print("Second parent selected.")
    return parent_a, parent_b


def normalise_values(fitness_values):
    """_summary_

    Args:
        fitness_values (_type_): _description_

    Returns:
        _type_: _description_
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


def choose_parent(range_limits):
    # problem parent set to 10 - not working with indexing
    """_summary_

    Args:
        range_limits (_type_): _description_

    Returns:
        _type_: _description_
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
