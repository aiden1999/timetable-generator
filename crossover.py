import random


def crossover(parent_a, parent_b, num_of_sessions):
    """_summary_

    Args:
        parent_a (_type_): _description_
        parent_b (_type_): _description_
        num_of_sessions (_type_): _description_

    Returns:
        _type_: _description_
    """
    print("Producing offspring...")
    offspring = []
    for i in range(5):  # hard coding - 10 offspring from 5 crossovers TODO
        # locus_outer: session that contains the split
        # locus_inner: split after session[locus_inner]
        locus_outer = random.randint(0, num_of_sessions - 1)
        if locus_outer == 0:
            locus_inner = random.randint(1, 2)  # hard coding TODO
        else:
            locus_inner = random.randint(0, 2)  # hard coding TODO

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
    print("Offspring produced.")
    return offspring
