from seating_chart.slide import make_slides, ET
from seating_chart.seats import make_tables, Student
import csv
from typing import Dict, List
from collections import defaultdict
from pathlib import Path
from dataclasses import dataclass

SCRIPT_DIR = Path(__file__).resolve().parent

@dataclass
class Content():
    agenda: dict
    do_now: dict
    announcements: dict
    seeds: dict

    @classmethod
    def from_dict(cls, d: dict):
        agenda = cls.to_default_dict(d["agenda"])
        do_now = cls.to_default_dict(d["do_now"])
        announcements = cls.to_default_dict(d["announcements"])
        seeds = d["seeds"]
        return cls(agenda, do_now, announcements, seeds)

    @staticmethod
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

def generate(periods: List[str], content: Content, max_table_size:int, exam_mode:bool):
    agenda = content.agenda
    announcements = content.announcements
    do_now = content.do_now
    seeds = content.seeds
    slide_filenames = []
    tables_by_period = dict()
    for period in periods:
        seed = seeds[period]
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