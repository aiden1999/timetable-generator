"""Phase 5 (mutation) of genetic algorithm.

Functions:
    mutate(offspring_in: list, time_slots: list, rooms: list, sessions: list,
        mutation_chance: int) -> list
"""
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
    # print("Mutating offspring...") TODO: remove probably
    mutation_count = 0
    offspring = offspring_in
    for solution in offspring:
        for session in solution:
            for i in range(3):
                mutate = random.randint(1, mutation_chance)

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
    # print("Offspring mutated. " + str(mutation_count) +
    #       " mutation(s) occurred.") TODO remove probably
    return offspring
