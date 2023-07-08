"""Phase 1 (initial population) of genetic algorithm.

Functions:
    get_config_data() -> [list, list, list]
    generate_initial_population(sessions: list, rooms: list, time_slots: list)
        -> list
    create_session_solution(session: list, rooms: list, time_slots: list)
        -> list
    create_complete_solution(sessions: list, rooms: list, time_slots: list)
        -> list
"""
import json
import random


def get_config_data() -> [list, list, list]:
    """Get the timetable data from data.json.

    Returns:
        list: Session consisting of module ID, student group and teacher.
        list: List of rooms.
        list: List of time slots.
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


def generate_initial_population(sessions: list, rooms: list,
                                time_slots: list) -> list:
    """Generate the first population randomly from the imported data.

    Args:
        sessions (list): List of sessions consisting of module ID, student
            group and teacher.
        rooms (list): List of rooms.
        time_slots (list): List of time slots.

    Returns:
        list: The generated population.
    """
    print("Generating initial population...")
    population = []
    for i in range(10):  # TODO: remove hard coding
        solution = create_complete_solution(sessions, rooms, time_slots)
        population.append(solution)
    print("Initial population generated.")
    return population


def create_session_solution(session: list, rooms: list, time_slots: list) \
     -> list:
    """Create a session, to become part of a solution.

    Args:
        session (list): A single session consisting of module ID, student
            group and teacher.
        rooms (list): List of rooms.
        time_slots (list): List of time slots.

    Returns:
        list: The complete session with time slot and room.
    """
    time_slot = random.choice(time_slots)
    room = random.choice(rooms)
    student_group = session[1]
    module = session[0]
    teacher = session[2]
    solution = [time_slot, room, student_group, module, teacher]
    return solution


def create_complete_solution(sessions: list, rooms: list, time_slots: list) \
         -> list:
    """Create a complete solution from a list of session solutions.

    Args:
        sessions (list): List of sessions consisting of module ID, student
            group and teacher.
        rooms (list): List of rooms.
        time_slots (list): List of time slots.

    Returns:
        list: A solution, which is a member of the population.
    """
    solution = []
    for session in sessions:
        session_solution = create_session_solution(session, rooms, time_slots)
        solution.append(session_solution)
    return solution
