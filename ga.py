import json
import random
import os


def generate_timetable():
    """Base function for the timetable generation.

    Basis of the timetable generation, goes through the whole of the
    genetic algorithm.
    """
    sessions, rooms, time_slots = get_config_data()
    population = generate_initial_population(sessions, rooms, time_slots)
    population_fitness, valid_solution_bool, valid_solution = \
        check_population_fitness(population)
    # works up to here TODO: remove later
    while not valid_solution_bool:
        print("No timetable solution found.")
        parent_a, parent_b = select_parents(population_fitness)
        # Note that parent_a and parent_b are indices
        offspring = crossover(population[parent_a],
                              population[parent_b], len(population[0]))
        # check if any of the offspring is a valid solution
        mutated_offspring = mutation(offspring, time_slots, rooms, sessions)
        new_pop = mutated_offspring + population[parent_a] + \
            population[parent_b]  # add to list
        print("New population:")
        print(new_pop)  # debugging TODO: remove later
        # TODO: there is some kind of problem with the next line
        population_fitness, valid_solution_bool, valid_solution \
            = check_population_fitness(new_pop)
        if not valid_solution_bool:  # TODO
            # combine new_pop and population_fitness into a 2D array (2 *12)
            new_pop_fitness = zip(new_pop, population_fitness)
            print(new_pop_fitness)  # debugging
            # sort by fitness
            # remove last 2
    print("Timetable solution found. Writing output to text files...")
    generate_output_text(valid_solution)
    print("Output written to files in ./teacher-timetables and \
    ./student-group-timetables.")
    # TODO: display valid solution or output to txt or something idk


def generate_output_text(solution):
    # TODO: add 'person' parameter to do teacher and student
    # session[0] = time_slot
    # session[1] = room
    # session[2] = student_group
    # session[3] = module
    # session[4] = teacher
    """_summary_

    Args:
        solution (_type_): _description_
    """

    teachers_dict = {}
    student_groups_dict = {}
    file = open("config.json", "r", encoding="utf-8")
    data = json.load(file)
    file.close()
    for teacher in data["teachers"]:
        teachers_dict.update({teacher["id"]: []})
    for student_group in data["student_groups"]:
        student_groups_dict.update({student_group["id"]: []})
    print(solution)  # debugging TODO: remove later
    for session in solution:
        # print("session: " + str(session))  # debugging TODO: remove later
        session_teacher = session[4]
        # print(session_teacher)  # debugging TODO: remove later
        session_teacher_list = teachers_dict.get(session_teacher)
        session_teacher_list.append(session)
        teachers_dict.update({session_teacher: session_teacher_list})
        session_student_group = session[2]
        session_student_group_list = student_groups_dict.get(
            session_student_group)
        session_student_group_list.append(session)
        student_groups_dict.update({session_student_group:
                                    session_student_group_list})
    print("Creating directory for teacher timetables...")
    try:
        os.mkdir("./teacher-timetables")
        print("Directory 'teacher-timetables' created.")
    except FileExistsError:
        print("Directory 'teacher-timetables' already exists.")
    for session_teacher in teachers_dict:
        file = open(str(session_teacher) + "-timetable.txt", "w",
                    encoding="utf-8")
        teacher_sessions = teachers_dict[session_teacher]
        for session in teacher_sessions:
            file.write(str(session))
        file.close()
    print("Timetable output files created.")
    # formatting?


# ==================== PHASE 1: INITIAL POPULATION ====================

def get_config_data():  # TODO: add ->
    """_summary_

    Returns:
        _type_: _description_
    """
    print("Reading config file")
    file = open("config.json", "r", encoding="utf-8")
    data = json.load(file)
    file.close()

    sessions, rooms_id, time_slots_id = [], [], []
    for module in data["modules"]:
        session = [module["id"], module["student_group"], module["teachers"]]
        for i in range(int(module["hours"])):
            sessions.append(session)

    for room in data["rooms"]:
        rooms_id.append(room["id"])

    day_number = 1
    for day in data["time_slots"]:
        for start_time in range(len(day["start_times"])):
            time_number = day["start_times"][start_time]
            time_slots_id.append(str(day_number) + str(time_number))
        day_number += 1

    return sessions, rooms_id, time_slots_id


def generate_initial_population(sessions, rooms, time_slots) -> list:
    """_summary_

    Args:
        sessions (_type_): _description_
        rooms (_type_): _description_
        time_slots (_type_): _description_

    Returns:
        list: _description_
    """
    print("Generating initial population...")
    population = []
    for i in range(10):  # TODO: remove hard coding
        solution = create_complete_solution(sessions, rooms, time_slots)
        population.append(solution)
    return population
    print("Initial population generated.")


def create_session_solution(session, rooms: list[str], time_slots: list[int]) \
     -> list:
    """_summary_

    Args:
        session (_type_): _description_
        rooms (list[str]): _description_
        time_slots (list[int]): _description_

    Returns:
        list: _description_
    """
    time_slot = random.choice(time_slots)
    room = random.choice(rooms)
    student_group = session[1]
    module = session[0]
    teacher = session[2]
    solution = [time_slot, room, student_group, module, teacher]
    return solution


def create_complete_solution(sessions, rooms, time_slots):
    """_summary_

    Args:
        sessions (_type_): _description_
        rooms (_type_): _description_
        time_slots (_type_): _description_

    Returns:
        _type_: _description_
    """
    solution = []
    for session in sessions:
        session_solution = create_session_solution(session, rooms, time_slots)
        solution.append(session_solution)
    return solution


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


# ==================== PHASE 3: SELECTION ====================

def select_parents(population_fitness):
    """_summary_

    Args:
        population_fitness (_type_): _description_

    Returns:
        _type_: _description_
    """
    print("Selecting parents for crossover...")
    fitness_values = population_fitness
    range_limits_a = normalise_values(fitness_values)
    parent_a = choose_parent(range_limits_a)
    print(str(parent_a))  # debugging TODO: remove later
    print("First parent selected.")
    fitness_values.remove(fitness_values[parent_a])
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
            parent_index = upper
        elif range_limits[middle] < choice:
            lower = middle
        else:
            upper = middle
    return parent_index


# ==================== PHASE 4: CROSSOVER ====================

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
    for i in range(5):  # hard coding
        locus_outer = random.randint(0, num_of_sessions - 1)
        if locus_outer == 0:
            locus_inner = random.randint(1, 2)  # hard coding
        else:
            locus_inner = random.randint(0, 2)  # hard coding

        # Crossover of child a
        left_a = parent_a[:locus_outer]
        centre_a = parent_a[locus_outer][:locus_inner] + \
            parent_b[locus_outer][locus_inner:]
        right_a = parent_b[locus_outer + 1:]
        child_a = [left_a, [centre_a], right_a]
        offspring.append(child_a)

        # Crossover of child b
        left_b = parent_b[:locus_outer]
        centre_b = parent_b[locus_outer][:locus_inner] + \
            parent_a[locus_outer][locus_inner:]
        right_b = parent_a[locus_outer + 1:]
        child_b = [left_b, [centre_b], right_b]
        offspring.append(child_b)
    print("Offspring produced.")
    return offspring


# ==================== PHASE 5: MUTATION ====================

def mutation(offspring_in, time_slots, rooms, sessions):
    """_summary_

    Args:
        offspring_in (_type_): _description_
        time_slots (_type_): _description_
        rooms (_type_): _description_
        sessions (_type_): _description_

    Returns:
        _type_: _description_
    """
    print("Mutating offspring...")
    mutation_count = 0
    offspring = offspring_in
    for solution in offspring:
        for session in solution:
            for i in range(3):  # hard coding
                mutate = random.randint(1, 1000)

                # Mutation does occur
                if mutate == 0:
                    mutation_count += 1
                    match i:

                        # Mutation of time slot
                        case 0:
                            new_time_slot = random.choice(time_slots)
                            offspring[solution][session][0] = new_time_slot

                        # Mutation of room
                        case 1:
                            new_room = random.choice(rooms)
                            offspring[solution][session][1] = new_room

                        # Mutation of session
                        case _:
                            new_session = random.choice(sessions)
                            offspring[solution][session][2] = new_session[0]
                            offspring[solution][session][3] = new_session[1]
                            offspring[solution][session][4] = new_session[2]
    print("Offspring mutated. " + str(mutation_count) + 
    " mutation(s) occured.")
    return offspring
