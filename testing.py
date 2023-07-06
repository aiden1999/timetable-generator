class Session:
    def __init__(self, time_slot, room, student_groups, module, teacher):
        self.time_slot = time_slot
        self.room = room
        self.student_groups = student_groups
        self.module = module
        self.teacher = teacher


class Timetable(list[Session]):
    def __init__(self):
        super().__init__()


session1 = Session("time1", "room1", "sg1", "mod1", "teacher1")
session2 = Session("time1", "room1", "sg1", "mod1", "teacher1")
session2.time_slot = "time2"
session2.room = "room2"
session2.student_groups = "sg2"
session2.module = "mod2"
session2.teacher = "teacher2"

timetable = Timetable()

timetable.append(session1)
timetable.append(session2)

for session in timetable:
    print(session)
