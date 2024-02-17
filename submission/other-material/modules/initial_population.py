"""Phase 1 (initial population) of genetic algorithm.

Functions:
    get_config_data() -> [list, list, list, list]
    generate_initial_population(sessions: list, rooms: list, time_slots: list,
        population_size: int) -> list
    create_session_solution(session: list, rooms: list, time_slots: list)
        -> list
    create_complete_solution(sessions: list, rooms: list, time_slots: list)
        -> list
"""
import json
import random


def get_config_data() -> [list, list, list, list]:
    """Get the timetable data from data.json.

    Returns:
        list: Session consisting of module ID, student group and teacher.
        list: List of rooms.
        list: List of time slots.
        list: List of teachers' preferred time slots.
    """
    file = open("data.json", "r", encoding="utf-8")
    data = json.load(file)
    file.close()

    sessions, rooms_id, time_slots_id = [], [], []
    for module in data["modules"]:
        session = [module["id"], module["student_group"], module["teachers"]]
        for i in range(int(module["lecture_hours"])):
            sessions.append(session)
        for i in range(int(module["lab_hours"])):
            sessions.append(session)

    for room in data["rooms"]:
        rooms_id.append(room["id"])

    day_number = 1
    for day in data["time_slots"]:
        for start_time in range(len(day["start_times"])):
            time_number = day["start_times"][start_time]
            time_slots_id.append(str(day_number) + str(time_number))
        day_number += 1

    teacher_times = {}
    for teacher in data["teachers"]:
        teacher_time = []
        teacher_id = (teacher["id"])
        for day in teacher["available_times"]:
            day_name = day["day"]
            match day_name:
                case "Monday":
                    day_number = 1
                case "Tuesday":
                    day_number = 2
                case "Wednesday":
                    day_number = 3
                case "Thursday":
                    day_number = 4
                case "Friday":
                    day_number = 5
                case "Saturday":
                    day_number = 6
                case "Sunday":
                    day_number = 7
                case _:
                    day_number = 0
            for i in range(len(day["start_times"])):
                time_number = day["start_times"][i]
                teacher_time.append(str(day_number) + str(time_number))
        teacher_times.update({teacher_id: teacher_time})

    return sessions, rooms_id, time_slots_id, teacher_times


def generate_initial_population(sessions: list, rooms: list,
                                time_slots: list, population_size: int) \
                                -> list:
    """Generate the first population randomly from the imported data.

    Args:
        sessions (list): List of sessions consisting of module ID, student
            group and teacher.
        rooms (list): List of rooms.
        time_slots (list): List of time slots.
        population_size (int): Size of the population.

    Returns:
        list: The generated population.
    """
    population = []
    for i in range(population_size):
        solution = create_complete_solution(sessions, rooms, time_slots)
        population.append(solution)
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
