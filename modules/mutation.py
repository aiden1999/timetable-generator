"""Phase 5 (mutation) of genetic algorithm.

Functions:
    mutate(offspring_in: list, time_slots: list, rooms: list, sessions: list,
        mutation_chance: int) -> list
"""
import copy
import random


def mutate(offspring_in: list, time_slots: list, rooms: list, sessions: list,
           mutation_chance: int) -> list:
    """Chance for offspring to mutate.

    Args:
        offspring_in (list): The pre-mutation offspring.
        time_slots (list): The list of time slots.
        rooms (list): The list of rooms.
        sessions (list): The list of sessions.
        mutation_chance (int): The chance of mutation.

    Returns:
        list: List of mutated offspring.
    """
    mutation_count = 0
    offspring = copy.copy(offspring_in)
    for i in range(len(offspring)):  # For each solution
        solution = offspring[i]
        for j in range(len(solution)):  # For each session
            for k in range(3):
                mutate = random.randint(1, mutation_chance)
                # Mutation does occur
                if mutate == 1:
                    mutation_count += 1
                    match k:
                        # Mutation of time slot
                        case 0:
                            new_time_slot = random.choice(time_slots)
                            offspring[i][j][0] = new_time_slot
                        # Mutation of room
                        case 1:
                            new_room = random.choice(rooms)
                            offspring[i][j][1] = new_room

                        # Mutation of session
                        case _:
                            new_session = random.choice(sessions)
                            offspring[i][j][2] = new_session[0]
                            offspring[i][j][3] = new_session[1]
                            offspring[i][j][4] = new_session[2]

    return offspring
