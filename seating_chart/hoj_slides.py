from seating_chart.slide import make_slides, ET
from seating_chart.seats import make_tables, Student
import csv
from typing import Dict, List
from collections import defaultdict
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

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

def generate(periods: List[str], content: Dict[str, Dict], max_table_size:int, exam_mode:bool, seed=None):
    agenda = to_default_dict(content["agenda"])
    announcements = to_default_dict(content["announcements"])
    do_now = to_default_dict(content["do_now"])
    slide_filenames = []
    tables_by_period = dict()
    for period in periods:
        students = load_roster(period)
        tables = make_tables(students, max_table_size=max_table_size, seed=seed)
        svg = make_slides(
            tables, 
            announcements=announcements[period],
            agenda = agenda[period],
            donows = do_now[period],
            exam_mode=exam_mode
        )
        xml_string = ET.tostring(svg, encoding='unicode')

        # Save the string to a file
        filename = f'welcome_slide_{seed}_{period}.svg'
        with open(filename, 'w') as f:
            f.write(xml_string)
            print(f"File '{f.name}' has been created.")
        slide_filenames.append(filename)
        tables_json = {f"Table_{k+1}":[x.name for x in tables[k]] for k in range(len(tables))}
        tables_by_period[period] = tables_json
    return tables_by_period, slide_filenames