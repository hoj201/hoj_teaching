from seating_chart.slide import make_slides, ET
from seating_chart.seats import make_kagan_tables, make_tables, Student
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

DEFAULT_TABLE_SIZES = {"period_12": 4, "period_45": 4, "period_78": 4, "period_910": 1}

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
        kagan = d.get("kagan", True)

        tables = cls.tables_from_json_dict(d.get("tables", dict()))
        max_table_size = d.get("max_table_size", DEFAULT_TABLE_SIZES)
        logger.info(f"Max table sizes: {max_table_size}")
        if "seeds" in d:
            seeds = cls.to_default_dict(d["seeds"])
            for period in PERIODS:
                if period in tables or (period not in seeds and "default" not in seeds):
                    continue
                seed = seeds[period]
                tables[period] = cls.tables_from_rng_seed(period, seed, max_table_size=max_table_size[period], kagan=kagan)
        for period in PERIODS:
            if period not in tables:
                logger.info(f"No tables or seed provided for {period}, loading default tables")
                tables[period] = cls.default_tables(period, max_table_size=max_table_size[period])
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
    def tables_from_rng_seed(period: str, seed: int, max_table_size: int = 4, kagan: bool = True) -> List[List[Student]]:
        logger.info(f"Generating tables for {period} with seed={seed}, max_table_size={max_table_size}, kagan={kagan}")
        students = load_roster(period)
        if kagan and max_table_size == 4:
            return make_kagan_tables(students, seed=seed)
        return make_tables(students, max_table_size=max_table_size, seed=seed)

    @staticmethod
    def default_tables(period: str, max_table_size: int = 3) -> List[List[Student]]:
        print(f"Loading default tables for {period} with max_table_size={max_table_size}")
        if max_table_size == 4:
            file_name = f'{SCRIPT_DIR}/default_tables_size4.json'
        elif max_table_size == 3:
            file_name = f'{SCRIPT_DIR}/default_tables.json'
        elif max_table_size == 2:
            file_name = f'{SCRIPT_DIR}/default_tables_size2.json'
        elif max_table_size == 1:
            file_name = f'{SCRIPT_DIR}/default_tables_size1.json'
        else:
            logger.warning("No default tables for max_table_size other than 2 or 3, outputing a random seating")
            return Content.tables_from_rng_seed(period, seed="default", max_table_size=max_table_size)
        with open(file_name, mode ='r') as file:
            tables_json = json.load(file)
        return Content.tables_from_json_dict(tables_json)[period]


def load_roster(period) -> List[Student]:
    students = list()
    with open(f'{SCRIPT_DIR}/rosters/{period}.csv', mode ='r')as file:
        csvFile = csv.DictReader(file)
        for row in csvFile:
                pref_seating = row["preferential_seating"].strip().lower()=='yes'
                student_dict = {
                    "name": row["first_name"],
                    "preferential_seating": pref_seating,
                    "avoids": row["avoids"].split(":"),
                    "level": row["level"]
                }
                students.append(Student.from_json_dict(student_dict))
    return students




def generate(periods: List[str], content: Content, printable: bool):
    agenda = content.agenda
    announcements = content.announcements
    do_now = content.do_now
    tables = content.tables
    slide_filenames = []
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