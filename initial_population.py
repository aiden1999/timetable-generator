import json
import random


def get_config_data() -> [list, list, list]:
    """_summary_

    Returns:
        [list, list, list]: _description_
    """
    print("Reading data file")
    file = open("data.json", "r", encoding="utf-8")
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
