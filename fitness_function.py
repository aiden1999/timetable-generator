# ==================== PHASE 2: FITNESS FUNCTION ====================

def check_population_fitness(population):
    """_summary_

    Args:
        population (_type_): _description_

    Returns:
        _type_: _description_
    """
    print("Calculating the fitness of individuals...")
    population_fitness = []
    valid_solution_bool = False
    valid_solution = None
    for solution in population:
        sol_fitness = calculate_fitness(solution)
        population_fitness.append(sol_fitness)
        if sol_fitness == 0:
            valid_solution_bool = True
            valid_solution = solution
            break
    print("Fitness of individuals calculated.")
    return population_fitness, valid_solution_bool, valid_solution


def calculate_fitness(solution):
    """_summary_

    Args:
        solution (_type_): _description_

    Returns:
        _type_: _description_
    """

    # Sort by time slot
    solution.sort(key=lambda x: x[0])
    clash_count = 0

    for i in range(len(solution) - 1):

        # Case where no sessions are happening at the same time
        if solution[i][0] != solution[i + 1][0]:
            pass

        else:

            # Room clash
            if solution[i][1] == solution[i + 1][1]:
                clash_count += 1
                pass

            # Student group clash
            if solution[i][2] == solution[i + 1][2]:
                clash_count += 1
                pass

            # Teacher clash
            if solution[i][4] == solution[i + 1][4]:
                clash_count += 1
                pass

    if clash_count == 0:
        fitness = 0
    else:
        fitness = 1 / clash_count
    return fitness
