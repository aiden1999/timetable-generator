import random

def choose_parent(range_limits):
    choice = random.random()
    print("choice: ", choice)  # debugging
    lower, upper = 0, len(range_limits) - 1
    found_parent = False
    while not found_parent:
        middle = (lower + upper) // 2
        print("lower: ", lower, " middle: ", middle, " upper: ", upper)  # debugging
        if lower == upper - 1:
            found_parent = True
            parent_index = upper
        elif range_limits[middle] < choice:
            lower = middle
        else:
            upper = middle
    return parent_index

limits = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
index = choose_parent(limits)
print("index " + str(index))