import random


def mutate(offspring_in, time_slots, rooms, sessions):
    """_summary_

    Args:
        offspring_in (_type_): _description_
        time_slots (_type_): _description_
        rooms (_type_): _description_
        sessions (_type_): _description_

    Returns:
        _type_: _description_
    """
    print("Mutating offspring...")
    mutation_count = 0
    offspring = offspring_in
    for solution in offspring:
        for session in solution:
            for i in range(3):  # hard coding
                mutate = random.randint(1, 1000)

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
    print("Offspring mutated. " + str(mutation_count) +
          " mutation(s) occured.")
    return offspring
