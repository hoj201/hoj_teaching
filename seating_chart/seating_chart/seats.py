import random
from typing import List, Set, Self


"""Code here takes in a list of student seating preferences and randomly
guesses table groupings until one works"""

class Student(object):
    def __init__(self, name: str, preferential_seating = False):
        self.name = name
        self.avoids : Set[Self] = set()
        self.preferential_seating = preferential_seating

    def __repr__(self):
        return f"Student({self.name})"

Table = Set[Student]


def swap_students(s1: Student, s2: Student, tables: List[Table]):
    t1, t2 = None, None
    for t in tables:
        if s1 in t:
            t1 = t
        if s2 in t:
            t2 = t
    assert(t1 is not None)
    assert(t2 is not None)
    t1.remove(s1)
    t2.add(s1)
    t2.remove(s2)
    t1.add(s2)

def random_swap(student: Student, tables: List[Table]):
    for table in tables:
        if student in tables:
            break
    other_tables = tables.copy()
    other_tables.remove(table)
    other_table = random.choice(other_tables)
    other_student = random.choice(list(other_table))
    swap_students(student, other_student, tables)


def make_tables(roster: List[Student], num_tables: int) -> List[Table]:
    # make random table groups
    # repeatedly find the most uncomfortable student and make a random swap until the total comfort stabilizes
    unassigned_students = roster[:] # copy so original isn't modified

    # Assign preferential seating students first to tables 0,1,2
    front_row_students = [s for s in unassigned_students if s.preferential_seating]
    random.shuffle(front_row_students)
    tables = [set() for _ in range(3)]
    for i, student in enumerate(front_row_students):
        tables[i % 3].add(student) # distribute evenly
        unassigned_students.remove(student)

    # Assign the remainder of the students
    for _ in range(num_tables-3):
        tables.append(set())
    random.shuffle(unassigned_students)      # randomize order
    for i, obj in enumerate(unassigned_students):
        index = i % num_tables
        if len(tables[index]) < 3:
            tables[i % num_tables].add(obj) # distribute evenly
    return tables


if __name__ == "__main__":
    students_names = ["john", "paul", "sartre", "linda", "lucile", "jacky"]    
    students = [Student(name) for name in students_names]
    print("{} avoids {}".format(students[3], students[0]))
    students[3].avoids.add(students[0])
    tables = make_tables(students, 3)
    print(tables)