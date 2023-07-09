"""Genetic algorithm base.

Functions:
    generate_timetable()
    get_settings_data() -> [int, int]
    generate_output_text(solution: list)
"""
import initial_population as p1
import fitness_function as p2
import selection as p3
import crossover as p4
import mutation as p5
import json


def generate_timetable():
    """Generate the timetable.

    Basis of the timetable generation, goes through the whole of the
    genetic algorithm.
    """
    population_size, mutation_chance = get_settings_data()
    sessions, rooms, time_slots = p1.get_config_data()
    population = p1.generate_initial_population(sessions, rooms, time_slots,
                                                population_size)
    population_fitness, valid_solution_bool, valid_solution = \
        p2.check_population_fitness(population)
    while not valid_solution_bool:
        print("No timetable solution found.")
        parent_a, parent_b = p3.select_parents(population_fitness)
        # Note that parent_a and parent_b are indices
        offspring = p4.crossover(population[parent_a], population[parent_b],
                                 len(population[0]), population_size)
        # check if any of the offspring is a valid solution
        mutated_offspring = p5.mutate(offspring, time_slots, rooms, sessions)
        mutated_offspring.append(population[parent_a])
        mutated_offspring.append(population[parent_b])
        population_fitness, valid_solution_bool, valid_solution \
            = p2.check_population_fitness(mutated_offspring)
        if not valid_solution_bool:
            population = mutated_offspring
            for i in range(2):
                worst_fitness = max(population_fitness)
                worst_fitness_index = population_fitness.index(worst_fitness)
                del population_fitness[worst_fitness_index]
                del population[worst_fitness_index]
    print("Timetable solution found. Writing output to text files...")
    generate_output_text(valid_solution)
    print("Output written to files in ./teacher-timetables and \
    ./student-group-timetables.")


def get_settings_data() -> [int, int]:
    """Get settings for timetable generation.

    Returns:
        int: Population size set by the user.
        int: Chance of mutation set by the user.
    """
    file = open("settings.json", "r", encoding="utf-8")
    settings = json.load(file)
    file.close()
    population_size = int(settings["population-size"])
    mutation_chance = int(settings["mutation-chance"])
    return population_size, mutation_chance


def generate_output_text(solution: list):
    # TODO: add 'person' parameter to do teacher and student
    # session[0] = time_slot
    # session[1] = room
    # session[2] = student_group
    # session[3] = module
    # session[4] = teacher
    """Generate output of a correct timetable to text files.

    Args:
        solution (list): A correct timetable solution.
    """
    teachers_dict = {}
    student_groups_dict = {}
    file = open("data.json", "r", encoding="utf-8")
    data = json.load(file)
    file.close()
    for teacher in data["teachers"]:
        teachers_dict.update({teacher["id"]: []})
    for student_group in data["student_groups"]:
        student_groups_dict.update({student_group["id"]: []})
    # print(solution)  # debugging TODO: remove later
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
    # TODO: formatting?
