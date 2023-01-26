import json


class Solution(str):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def calculate_fitness():
        pass
    
    def crossover():
        pass
    
    def mutation():
        pass
    

def generate_timetable():
    print("Generating initial population")
    generate_initial_population()
    
def get_config_data():
    print("Reading config file")
    file = open("config.json", "r")
    data = json.load(file)
    teachers = data["teachers"]
    rooms = data["rooms"]
    student_groups = data["student_groups"]
    modules = data["modules"]
    time_slots = data["time_slots"]
    file.close()
    return teachers, rooms, student_groups, modules, time_slots
    

def generate_initial_population():
    teachers, rooms, student_groups, modules, time_slots = get_config_data()
    teachers_id = []
    for teacher in teachers:
        teachers_id.append(teacher["id"])
    rooms_id = []
    for room in rooms:
        rooms_id.append(room["id"])
    student_groups_id = []
    for student_group in student_groups:
        student_groups_id.append(student_group["id"])
    modules_id = []
    for module in modules:
        modules_id.append(module["id"])
    