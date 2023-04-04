import json
import random


def generate_timetable():
    print("Generating initial population...")
    sessions, rooms, time_slots = get_config_data()
    population = generate_initial_population(sessions, rooms, time_slots)
    population_fitness, valid_solution = check_population_fitness(population)
    while not valid_solution:
        parent_a, parent_b = select_parents(population_fitness)
        offspring = crossover(population[parent_a],
                              population[parent_b], len(population[0]))
        # check if any of the offspring is a valid solution
        mutated_offspring = mutation(offspring, time_slots, rooms, sessions)
        new_pop = mutated_offspring + population[parent_a] + population[parent_b]  # add to list
        population_fitness, valid_solution = check_population_fitness(new_pop)
        if not valid_solution:
            # combine new_pop and population_fitness into a 2D array (2 *12)
            # sort by fitness
            # remove last 2
            pass
    print("Timetable solution found. Output in timetable.txt")
    # display valid solution or output to txt or something idk


def get_config_data():
    print("Reading config file")
    file = open("config.json", "r")
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
    population = []
    for i in range(10):  # hard coding
        solution = create_complete_solution(sessions, rooms, time_slots)
        population.append(solution)
    return population


def create_session_solution(session, rooms: list[str], time_slots: list[int]) -> list:
    time_slot = random.choice(time_slots)
    room = random.choice(rooms)
    student_group = session[1]
    module = session[0]
    teacher = session[2]
    solution = [time_slot, room, student_group, module, teacher]
    return solution


def create_complete_solution(sessions, rooms, time_slots):
    solution = []
    for session in sessions:
        session_solution = create_session_solution(session, rooms, time_slots)
        solution.append(session_solution)
    return solution


def check_population_fitness(population):
    population_fitness = []
    valid_solution = False
    for solution in population:
        sol_fitness = calculate_fitness(solution)
        population_fitness.append(sol_fitness)
        if sol_fitness == 0:
            valid_solution = True
            break
    print("generation done")
    return population_fitness, valid_solution


def calculate_fitness(solution):

    # Sort by time slot
    print("solution: ", solution)  # there is a bug here v
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
    print(fitness)
    return fitness


def select_parents(population_fitness):
    fitness_values = population_fitness
    range_limits_a = normalise_values(fitness_values)
    print("range_limits_a: ", range_limits_a)  # there is a bug here v
    parent_a = choose_parent(range_limits_a)
    print("parent a ", parent_a)  # there was a bug here v
    fitness_values.remove(fitness_values[parent_a])
    range_limits_b = normalise_values(fitness_values)
    parent_b = choose_parent(range_limits_b)
    return parent_a, parent_b


def normalise_values(fitness_values):
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
    return range_limits


def choose_parent(range_limits):
    choice = random.random()
    print("choice: ", choice)  # debugging
    lower, upper = 0, len(range_limits) - 1
    found_parent = False
    while not found_parent:
        middle = (lower + upper) // 2
        print("lower: ", lower, " middle: ", middle, " upper: ", upper)  # debugging
        if lower == upper - 1:
            found_parent = True
            parent_index = upper
        elif range_limits[middle] < choice:
            lower = middle
        else:
            upper = middle
    return parent_index


def crossover(parent_a, parent_b, num_of_sessions):
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

    return offspring


def mutation(offspring_in, time_slots, rooms, sessions):
    offspring = offspring_in
    for solution in offspring:
        for session in solution:
            for i in range(3):  # hard coding
                mutate = random.randint(1, 1000)

                # Mutation does occur
                if mutate == 0:
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

    return offspring
