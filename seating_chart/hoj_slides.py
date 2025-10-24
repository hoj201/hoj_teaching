from seating_chart.slide import make_slides, ET
from seating_chart.seats import make_tables, Student
import csv
from typing import Dict, List
from collections import defaultdict
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

periods = [
    "period_12",
    "period_45",
    "period_78",
    "period_910"
]

def to_default_dict(d: Dict):
    output = defaultdict(lambda : d["default"])
    for k, v, in d.items():
         output[k] = v
    return output

def load_roster(period) -> List[Student]:
    students = list()
    with open(f'{SCRIPT_DIR}/rosters/{period}.csv', mode ='r')as file:
        csvFile = csv.DictReader(file)
        for row in csvFile:
                pref_seating = row["preferential_seating"].strip().lower()=='yes'
                students.append(
                    Student(
                        name=row["first_name"],
                        preferential_seating=pref_seating,
                        avoids=row["avoids"]
                    )
                )
    return students

def generate(agenda: Dict[str,List], announcements: Dict[str, List], do_now: Dict[str, List], seed=None):
    agenda = to_default_dict(agenda)
    announcements = to_default_dict(announcements)
    do_now = to_default_dict(do_now)
    for period in periods:
        students = load_roster(period)
        tables = make_tables(students, 3, seed=seed)
        svg = make_slides(
            tables, 
            announcements=announcements[period],
            agenda = agenda[period],
            donows = do_now[period]
        )
        xml_string = ET.tostring(svg, encoding='unicode')

        # Save the string to a file
        with open(f'welcome_slide_{seed}_{period}.svg', 'w') as f:
            f.write(xml_string)
            print(f"File '{f.name}' has been created.")