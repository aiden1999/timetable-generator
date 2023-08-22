"""Phase 2 (fitness function) of genetic algorithm.

Functions:
    check_population_fitness(population: list, teacher_times: list) -> [list,
        bool, list]
    check_fitness_only(population: list, teacher_times: list) -> list
    calculate_fitness(solution: list, teacher_times: list) -> int
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
    population_fitness = []
    valid_solution_bool = False
    valid_solution = None
    
    for solution in population:
        sol_fitness = calculate_fitness(solution, teacher_times)
        population_fitness.append([solution, sol_fitness])
        if sol_fitness == 0:
            valid_solution_bool = True
            valid_solution = solution
            break

    return population_fitness, valid_solution_bool, valid_solution


def check_fitness_only(population: list, teacher_times: list) -> list:
    """Check the fitness of the population.

    Does not return if there is a valid solution, and what it is if it exists.

    Args:
        population (list): The population of solutions.
        teacher_times (list): The time slot preferences of the teachers.

    Returns:
        list: The fitness values of the population.
    """
    population_fitness = []
    for solution in population:
        sol_fitness = calculate_fitness(solution, teacher_times)
        population_fitness.append([solution, sol_fitness])
    return population_fitness


def calculate_fitness(solution: list, teacher_times: list) -> float:
    """Calculate fitness of a solution.

    Args:
        solution (list): A possible solution to the timetabling problem.
        teacher_times (list): The time slot preferences of the teachers.

    Returns:
        int: Fitness of the solution.
    """
    # Sort by time slot
    solution_sorted = solution
    solution_sorted.sort(key=lambda x: x[0])
    problem_count = 0

    for i in range(len(solution_sorted) - 1):
        # Check if sessions are happening at the same time
        if solution_sorted[i][0] == solution_sorted[i + 1][0]:
            # Room clash:
            if solution_sorted[i][1] == solution_sorted[i + 1][1]:
                problem_count += 1
            # Student group clash:
            if solution_sorted[i][2] == solution_sorted[i + 1][2]:
                problem_count += 1
            # Teacher clash:
            if solution_sorted[i][4] == solution_sorted[i + 1][4]:
                problem_count += 1
    # Check teacher preferences
    for i in range(len(solution_sorted)):
        time_slot = solution_sorted[i][0]
        teacher_num = str(solution_sorted[i][4])
        teacher_prefs = teacher_times.get(teacher_num)
        if time_slot not in teacher_prefs:
            problem_count += 1
    return problem_count
