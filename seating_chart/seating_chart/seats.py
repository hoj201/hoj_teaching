import random
from typing import List, Set, Self, Tuple, Optional


"""Code here takes in a list of student seating preferences and randomly
guesses table groupings until one works"""

class Student(object):
    def __init__(self, name: str, preferential_seating = False, avoids: Optional[str] = None):
        self.name = name
        self.avoids = avoids
        self.preferential_seating = preferential_seating

    def __repr__(self):
        return f"Student({self.name})"

Table = Set[Student]

def bad_table(table: Table):
    for s1 in table:
        for s2 in table:
            if s1.avoids == s2.name:
                return True
    return False

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


def make_tables(roster: List[Student], max_table_size: int, seed: Optional[str]=None) -> List[Table]:
    if seed:
        random.seed(seed)
    unassigned_students = roster[:] # copy so original isn't modified
    num_tables = len(roster) // max_table_size
    if len(roster) % max_table_size != 0:
        num_tables += 1

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
    while len(unassigned_students) > 0:
        student = unassigned_students.pop()
        smallest_table = min(*tables, key = lambda x: len(x))
        smallest_table.add(student)
    if any([bad_table(t) for t in tables]):
        return make_tables(roster=roster, max_table_size=max_table_size, seed=seed + "67")
    return tables
