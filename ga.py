"""Genetic algorithm base.

Functions:
    generate_timetable()
    get_settings_data() -> [int, int]
    generate_output_text(solution: list, person_type: str)
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
    sessions, rooms, time_slots, teacher_times = p1.get_config_data()
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
    generate_output_text(valid_solution, "teachers")
    generate_output_text(valid_solution, "student_groups")
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


def generate_output_text(solution: list, person_type: str):
    """Generate output of a correct timetable to text files.

    Args:
        solution (list): A correct timetable solution.
        person_type (str): Who the timetable is for, student_groups or teachers
    """
    dictionary = {}
    file = open("data.json", "r", encoding="utf-8")
    data = json.load(file)
    file.close()

    for person in data[person_type]:
        dictionary.update({person["id"]: []})
    for session in solution:
        if person_type == "teachers":
            session_person = session[4]
        else:  # session_person == "student_groups"
            session_person = session[2]
        session_person_list = dictionary.get(session_person)
        session_person_list.append(session)
        dictionary.update({session_person: session_person_list})

    print("Creating directory for " + str(person_type) + " timetables...")
    try:
        os.mkdir("./" + str(person_type) + "_timetables")
        print("Directory '" + str(person_type) + "_timetables' created.")
    except FileExistsError:
        print("Directory already exists.")
    for session_person in dictionary:
        file = open(str(session_person) + ".txt", "w", encoding="utf-8")
        person_sessions = dictionary[session_person]
        for session in person_sessions:
            file.write(str(session))
        file.close()
    print("Timetable output files created.")
    # TODO: formatting?
