import json
import random


def generate_timetable():
    print("Generating initial population")
    population = generate_initial_population()
    for solution in population:
        sol_fitness = calculate_fitness(solution)
        print(sol_fitness)  # delete later


def get_config_data():
    print("Reading config file")
    file = open("config.json", "r")
    data = json.load(file)
    file.close()
    return data


def generate_initial_population():
    data = get_config_data()

    sessions = []
    for module in data["modules"]:
        session = [module["id"], module["student_group"], module["teachers"]]
        for i in range(int(module["hours"])):
            sessions.append(session)

    rooms_id = []
    for room in data["rooms"]:
        rooms_id.append(room["id"])

    time_slots_id = []
    day_number = 1
    for day in data["time_slots"]:
        for start_time in range(len(day["start_times"])):
            time_number = day["start_times"][start_time]
            time_slots_id.append(str(day_number) + str(time_number))
        day_number += 1

    population = []
    for i in range(10):
        solution = create_complete_solution(sessions, rooms_id, time_slots_id)
        population.append(solution)

    return population


def create_session_solution(session, rooms: list[str], time_slots: list[int]):
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


def calculate_fitness(solution):
    solution.sort(key=lambda x: x[0])  # sort by time slot
    clash_count = 0
    for i in range(len(solution) - 1):
        if solution[i][0] != solution[i + 1][0]:  # no sessions happening at the same time
            pass
        else:
            if solution[i][1] == solution[i + 1][1]:  # room clash
                clash_count += 1
                pass
            if solution[i][2] == solution[i + 1][2]:  # student group clash
                clash_count += 1
                pass
            if solution[i][4] == solution[i + 1][4]:  # teacher clash
                clash_count += 1
                pass
    if clash_count == 0:
        fitness = 0
    else:
        fitness = 1 / clash_count    
    return fitness 

def crossover():
    pass  # delete later


def mutation():
    pass  # delete later
