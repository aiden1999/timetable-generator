"""Phase 2 (fitness function) of genetic algorithm.

Functions:
    check_population_fitness(population: list, teacher_times: list) -> [list,
        bool, list]
    calculate_fitness(solution: list, teacher_times: list) -> float
"""


def check_population_fitness(population: list, teacher_times: list) \
        -> [list, bool, list]:
    """Calculate the fitness of the whole population.

    Args:
        population (list): The population of solutions.
        teacher_times (list): The time slot preferences of the teachers.

    Returns:
        list: The fitness values of the population.
        bool: Whether or not there is a correct solution.
        list: The correct solution (if it exists).
    """
    # print("Calculating the fitness of individuals...") TODO: add back
    population_fitness = []
    valid_solution_bool = False
    valid_solution = None

    for solution in population:
        sol_fitness = calculate_fitness(solution, teacher_times)
        population_fitness.append(sol_fitness)
        if sol_fitness == 0:
            valid_solution_bool = True
            valid_solution = solution
            break

    # print("Fitness of individuals calculated.") TODO: add back
    return population_fitness, valid_solution_bool, valid_solution


def calculate_fitness(solution: list, teacher_times: list) -> float:
    """Calculate fitness of a solution.

    Args:
        solution (list): A possible solution to the timetabling problem.
        teacher_times (list): The time slot preferences of the teachers.

    Returns:
        float: Fitness of the solution.
    """
    # Sort by time slot
    solution.sort(key=lambda x: x[0])
    problem_count = 0

    for i in range(len(solution) - 1):

        # Check if sessions are happening at the same time
        if solution[i][0] == solution[i + 1][0]:

            # Room clash:
            if solution[i][1] == solution[i + 1][1]:
                problem_count += 1

            # Student group clash:
            if solution[i][2] == solution[i + 1][2]:
                problem_count += 1

            # Teacher clash:
            if solution[i][4] == solution[i + 1][4]:
                problem_count += 1

    for i in range(len(solution)):

        # check teacher preferences
        time_slot = solution[i][0]
        teacher_num = int(solution[i][4])
        # TODO: why the FUCK is this not finished??????

    if problem_count == 0:
        fitness = 0
    else:
        fitness = 1 / problem_count
    return fitness
