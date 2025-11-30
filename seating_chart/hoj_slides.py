from seating_chart.slide import make_slides, ET
from seating_chart.seats import make_tables, Student
import csv, json
from typing import Dict, List
from collections import defaultdict
from pathlib import Path
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

SCRIPT_DIR = Path(__file__).resolve().parent
PERIODS = [
    "period_12",
    "period_45",
    "period_78",
    "period_910"
]

@dataclass
class Content():
    agenda: dict
    do_now: dict
    announcements: dict
    tables: dict

    @classmethod
    def from_dict(cls, d: dict):
        agenda = cls.to_default_dict(d["agenda"])
        do_now = cls.to_default_dict(d["do_now"])
        announcements = cls.to_default_dict(d["announcements"])

        tables = cls.tables_from_json_dict(d.get("tables", dict()))
        if "seeds" in d:
            seeds = cls.to_default_dict(d["seeds"])
            max_table_size = cls.to_default_dict(d["max_table_size"])
            for period in PERIODS:
                if period in tables:
                    continue
                seed = seeds[period]
                mts = max_table_size[period]
                tables[period] = cls.tables_from_rng_seed(period, seed, mts)
        for period in PERIODS:
            if period not in tables:
                tables[period] = cls.default_tables(period)
        return cls(agenda, do_now, announcements, tables)

    @staticmethod
    def to_default_dict(d: Dict):
        output = defaultdict(lambda : d["default"])
        for k, v, in d.items():
            output[k] = v
        return output

    @staticmethod
    def tables_from_json_dict(tables_json: Dict[str,List[List[str]]]) -> Dict[str, List[List[Student]]]:
        tables_by_period = dict()
        for period, tables_list in tables_json.items():
            tables = list()
            for table in tables_list:
                table_students = [Student(name) for name in table]
                tables.append(table_students)
            tables_by_period[period] = tables
        return tables_by_period          

    @staticmethod    
    def tables_from_rng_seed(period: str, seed: int, max_table_size) -> List[List[Student]]:
        students = load_roster(period)
        tables = make_tables(students, max_table_size=max_table_size, seed=seed)
        return tables

    @staticmethod
    def default_tables(period: str) -> List[List[Student]]:
        with open(f'{SCRIPT_DIR}/default_tables.json', mode ='r') as file:
            tables_json = json.load(file)
        return Content.tables_from_json_dict(tables_json)[period]


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




def generate(periods: List[str], content: Content, printable: bool):
    agenda = content.agenda
    announcements = content.announcements
    do_now = content.do_now
    tables = content.tables
    slide_filenames = []
    tables_by_period = dict()
    for period in periods:
        svg = make_slides(
            tables[period], 
            announcements=announcements[period],
            agenda = agenda[period],
            donows = do_now[period],
            printable=printable
        )
        xml_string = ET.tostring(svg, encoding='unicode')

        # Save the string to a file
        filename = f'welcome_slide_{period}.svg'
        with open(filename, 'w') as f:
            f.write(xml_string)
            logger.info(f"File '{f.name}' has been created.")
        slide_filenames.append(filename)
    tables_json = {period: [[x.name for x in table] for table in tables[period]] for period in periods}
    return tables_json, slide_filenames