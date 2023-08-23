"""Genetic algorithm base.

Functions:
    generate_timetable()
    get_settings_data() -> [int, int]
    generate_output_text(solution: list, person_type: str)
"""
import modules.initial_population as p1
import modules.fitness_function as p2
import modules.selection as p3
import modules.crossover as p4
import modules.mutation as p5
import json
import copy
import os


def generate_timetable():
    """Generate the timetable.

    Basis of the timetable generation, goes through the whole of the
    genetic algorithm.
    """
    population_size, mutation_chance = get_settings_data()
    sessions, rooms, time_slots, teacher_times = p1.get_config_data()
    print("Generation: 1")
    generation_count = 1
    population = p1.generate_initial_population(sessions, rooms, time_slots,
                                                population_size)
    population_fitness, valid_solution_bool, valid_solution = \
        p2.check_population_fitness(population, teacher_times)

    while not valid_solution_bool:

        parents, worst_parent_fitness = p3.select_parents(population_fitness,
                                                          population_size)

        offspring, parents_copy = p4.crossover(parents)

        offspring_fitness = p2.check_fitness_only(offspring, teacher_times)
        mutate_list = []
        not_mutate_list = []
        for solution in offspring_fitness:
            if solution[1] >= worst_parent_fitness:
                mutate_list.append(solution[0])
            else:
                not_mutate_list.append(solution[0])

        mutated = p5.mutate(mutate_list, time_slots, rooms, sessions,
                            mutation_chance)

        new_pop = []
        for solution in mutated:
            new_pop.append(solution)
        for solution in parents_copy:
            new_pop.append(solution)
        for solution in not_mutate_list:
            new_pop.append(solution)

        # check if any of the offspring is a valid solution
        new_pop_fitness, valid_solution_bool, valid_solution \
            = p2.check_population_fitness(new_pop, teacher_times)

        if not valid_solution_bool:
            new_pop_fitness.sort(key=lambda x: x[1])
            while len(new_pop) > population_size:
                worst_sol = new_pop_fitness[-1][0]
                new_pop.remove(worst_sol)
                del new_pop_fitness[-1]
            generation_count += 1
            print("Generation: " + str(generation_count))
            population = new_pop
            population_fitness = new_pop_fitness

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
