import random
from typing import List, Set, Self


"""Code here takes in a list of student seating preferences and randomly
guesses table groupings until one works"""

class Student(object):
    def __init__(self, name: str):
        self.name = name
        self.avoids : Set[Self] = set()

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
    shuffled = roster[:]         # copy so original isn’t modified
    random.shuffle(shuffled)      # randomize order
    
    tables = [set() for _ in range(num_tables)]
    for i, obj in enumerate(shuffled):
        tables[i % num_tables].add(obj) # distribute evenly
    return tables


if __name__ == "__main__":
    students_names = ["john", "paul", "sartre", "linda", "lucile", "jacky"]    
    students = [Student(name) for name in students_names]
    print("{} avoids {}".format(students[3], students[0]))
    students[3].avoids.add(students[0])
    tables = make_tables(students, 3)
    print(tables)